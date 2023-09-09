from __future__ import annotations
import asyncio
import craftlink
import json
import logging
from collections import deque
from pathlib import Path

from craftlink.constants import (
    ADMIN_COMMANDS,
    ADMIN_COMMAND_NAMES,
    ALL_COMMAND_NAMES,
    BEDROCK_COMMAND_NAMES,
    CMD_PREFIX,
)


LOGGER = logging.getLogger(__name__)


class Commander():
    """
    Class to dispatch commands, both to the bedrock server and administratively,
    e.g. commands that control the server itself (starting, updating settings).
    """
    def __init__(
        self,
        bot: craftlink.bot.CraftBot,
        server_path: Path,
        server_message_queue: deque
    ) -> None:
        self.bedrock_server_proc = None
        self.bot = bot
        self.server_message_queue = server_message_queue
        if not server_path.is_dir():
            raise ValueError("The given server directory is invalid.")
        self.server_path = server_path
        self.server_sh = server_path / "bedrock_server.exe"
        self.allowlist_file = server_path / "allowlist.json"
        # Verify no commands have been added for which we have no method.
        for command_name in ADMIN_COMMAND_NAMES:
            assert hasattr(self, f"_cmd_{command_name}")

    @property
    async def bedrock_server_running(self) -> bool:
        """Check if the Bedrock server process is active or exists."""
        if not self.bedrock_server_proc:
            return False
        else:
            return self.bedrock_server_proc.returncode is None

    async def _cmd_listcommands(self, args: list[str]) -> str:
        """
        List available commands. Can specify admin or server commands, otherwise
        defaults to sending all.
        """
        category = args[0]
        admin_commands = [
            (
                f'- `{CMD_PREFIX}{command_name}'
                f'{" " if info["args"] else ""}{info["args"]}`'
                f'\n  - {info["help"]}'
            )
            for command_name, info
            in ADMIN_COMMANDS.items()
        ]
        admin_commands = "\n".join(admin_commands)
        admin_cmd_help = f"**Administrative Commands** \n{admin_commands}"
        bedrock_commands = "\n- ".join(
            [f"`{CMD_PREFIX}{i}`" for i in BEDROCK_COMMAND_NAMES]
        )
        bedrock_cmd_help = f"**Bedrock Server Commands**\n- {bedrock_commands}"
        if category == "admin":
            commands_message = admin_cmd_help
        elif category == "server":
            commands_message = bedrock_cmd_help
        else:
            commands_message = admin_cmd_help + "\n\n" + bedrock_cmd_help
        return commands_message

    async def _cmd_adduser(self, args: list[str]) -> str:
        """Add a user to the server's allowlist.json file."""
        user_name = str(args[0])
        user_xuid = str(args[1])
        allowlist = json.loads(self.allowlist_file.read_text())
        if any(
            (i["name"] == user_name or i["xuid"] == user_xuid)
            for i in allowlist
        ):
            return "New user appears to be a duplicate user."
        new_entry = {
            "ignoresPlayerLimit": False,
            "name": user_name,
            "xuid": user_xuid,
        }
        allowlist.append(new_entry)
        self.allowlist_file.write_text(json.dumps(allowlist))
        return f"Added user {user_name} ({user_xuid}) to allowlist."

    async def _cmd_rmuser(self, args: list[str]) -> str:
        """Remove a user from the server's allowlist.json file."""
        user_name = str(args[0])
        allowlist = json.loads(self.allowlist_file.read_text())
        if not any(i["name"] == user_name for i in allowlist):
            return f"User *\"{user_name}\"* does not appear in allowlist."
        good_entries = [i for i in allowlist if i["name"] != user_name]
        self.allowlist_file.write_text(json.dumps(good_entries))
        return f"Removed user {user_name} from allowlist."

    async def _cmd_userrole(self, args: list[str]) -> str:
        return "Not yet implemented."

    async def _cmd_changeprop(self, args: list[str]) -> str:
        return "Not yet implemented."

    async def _cmd_showsettings(self, args: list[str]) -> str:
        target_file = args[0]
        if target_file == "allowlist":
            file_path = self.allowlist_file
        elif target_file == "permissions":
            file_path = self.server_path / "permissions.json"
        elif target_file == "properties":
            file_path = self.server_path / "server.properties"
        else:
            return f"Unrecognised file identifier *\"{target_file}\"*."
        file_contents = file_path.read_text()
        return f"**{file_path.name}**\n```{file_contents}```"

    async def _cmd_startserver(self, args: list[str] | None) -> str:
        """Launch and assign the Bedrock server process."""
        if await self.bedrock_server_running:
            return "The Bedrock server already running."
        self.bedrock_server_proc = (
            await asyncio.subprocess.create_subprocess_exec(
                str(self.server_sh.absolute()),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
            )
        )
        return "Started Bedrock server."

    async def _cmd_stopserver(self, args: list[str] | None) -> str:
        """
        Gracefully stop the Bedrock server by sending the `/stop` command.
        This command is mostly just for consistency since sending `/stop`
        does the same thing.
        """
        if not await self.bedrock_server_running:
            return "The Bedrock server is already shutdown."
        await self.send_bedrock_command("stop")
        return "Shutdown Bedrock server gracefully."

    async def _cmd_killserver(self, args: list[str] | None) -> str:
        """Force stop the Bedrock server process."""
        try:
            self.bedrock_server_proc.kill()
        except Exception:
            pass
        return "Shutdown Bedrock server forcefully."

    async def send_bedrock_command(
        self,
        command: str,
        user_name: str = "unknown",
    ) -> None:
        """
        Send a bedrock server command. This command does not return a message
        as some commands sent to the server need no confirmation (e.g. `/say`),
        however, if the server does give some reply, it'll be picked up and
        enqueued in the `Commander.poll_server_messages`.
        """
        if not await self.bedrock_server_running:
            return "The Bedrock server isn't running."
        # Append the Discord username to the "say" command.
        if command.startswith("say"):
            command = f'say ({user_name}@Discord){command[3:]}'
        encoded_command = bytes(command, encoding="utf-8") + b"\n"
        self.bedrock_server_proc.stdin.write(encoded_command)

    async def poll_server_messages(self) -> None:
        """Poll the server's output and enqueue any new messages."""
        while True:
            LOGGER.debug("Polling for server messages...")
            await asyncio.sleep(1)
            if not await self.bedrock_server_running:
                continue
            # All stdout.<read> methods will hang waiting for an EOF so
            # using a loop to grab everythign available and then letting
            # it hang while nothing is being sent.
            while True:
                try:
                    buffer = await self.bedrock_server_proc.stdout.readuntil(
                        b"\r\n"
                    )
                except asyncio.exceptions.IncompleteReadError:
                    break
                if "Running AutoCompaction" not in str(buffer):
                    self.server_message_queue.append(buffer)

    async def dispatch_command(
        self,
        command: str,
        user_name: str
    ) -> str | None:
        """Parse command and dispatch to target method."""
        message = ""
        command_and_args = command.split(" ")
        base_command = command_and_args[0]
        command_args = command_and_args[1:]
        if base_command not in ALL_COMMAND_NAMES:
            message = (
                f"Command `{base_command}` is not a valid command."
                f" Run `{CMD_PREFIX}listcommands` to list all commands."
            )
        elif base_command in BEDROCK_COMMAND_NAMES:
            if not await self.bedrock_server_running:
                message = (
                    f"Bedrock server not running... start it with the"
                    f" `{CMD_PREFIX}startserver` command and try again."
                )
            else:
                message = await self.send_bedrock_command(command, user_name)
        else:
            command_method = getattr(self, f"_cmd_{base_command}")
            try:
                message = await command_method(command_args)
            except Exception:
                LOGGER.info(
                    f"Command failed. Full command: {command}",
                    exc_info=True
                )
                message = (
                    "Something went wrong... verify the command's syntax and"
                    " try again. The error has been logged."
                )
        return message
