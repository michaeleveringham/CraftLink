from __future__ import annotations
import asyncio
import json
import logging
import os
import re
from collections import deque
from pathlib import Path

from craftlink.constants import (
    ADMIN_COMMANDS_MESSAGE,
    ADMIN_COMMAND_NAMES,
    ALL_COMMAND_NAMES,
    BEDROCK_COMMANDS_MESSAGE,
    BEDROCK_COMMAND_NAMES,
    CMD_PREFIX,
    IGNORED_MESSAGE_PATTERNS,
    JAVA_COMMANDS_MESSAGE,
    JAVA_COMMAND_NAMES,
    OS,
)


LOGGER = logging.getLogger(__name__)


class CraftCommander():
    """
    Class to dispatch commands, both to the server and administratively,
    e.g. commands that control the server itself (starting, updating settings).
    """
    def __init__(
        self,
        server_path: Path,
        server_message_queue: deque,
        server_type: str,
        java_mem_range: tuple[int],
    ) -> None:
        self.server_type = server_type
        self.server_proc = None
        self.server_message_queue = server_message_queue
        if not server_path.is_dir():
            raise ValueError("The given server directory is invalid.")
        self.server_path = server_path
        self.env = dict(os.environ)
        # Set the end of line character(s) for reading from the console.
        if OS == "windows":
            self.eol = b"\r\n"
        else:
            self.eol = b"\n"
        # Set the command based on os and server type.
        if server_type == "bedrock":
            if OS == "windows":
                server_binary = server_path / "bedrock_server.exe"
                self.server_cmd = str(server_binary.absolute())
                self.server_cmd = self.server_cmd.replace("\\", "/")
            else:
                server_binary = server_path / "bedrock_server"
                self.server_cmd = "./bedrock_server"
                self.env["LD_LIBRARY_PATH"] = str(self.server_path.absolute())
        elif server_type == "java":
            server_binary = server_path / "server.jar"
            mem_min, mem_max = java_mem_range
            self.server_cmd = (
                f"java -Xmx{mem_min}M -Xms{mem_max}M -jar server.jar nogui"
            )
        else:
            raise ValueError(f"Invalid server type given, {server_type}.")
        if not server_binary.is_file():
            raise FileNotFoundError(f"Cannot find {server_binary.absolute()}.")
        self.allowlist_file = server_path / "allowlist.json"
        # Default to whitelist if no allowlist.
        if not self.allowlist_file.is_file():
            self.allowlist_file = server_path / "whitelist.json"
        # Verify no commands have been added for which we have no method.
        for command_name in ADMIN_COMMAND_NAMES:
            assert hasattr(self, f"_cmd_{command_name}")

    @property
    async def server_running(self) -> bool:
        """Check if the server process is active or exists."""
        if not self.server_proc:
            return False
        else:
            return self.server_proc.returncode is None

    async def _cmd_listcommands(self, category: str = None, *args) -> str:
        """
        List available commands. Can specify admin or server commands,
        otherwise defaults to sending all.
        """
        if not category:
            commands_message = (
                f"{ADMIN_COMMANDS_MESSAGE}"
                "\n\nUse `!listcommands bedrock` or `!listcommands java`"
                " to show server commands."
            )
        elif category == "admin":
            commands_message = ADMIN_COMMANDS_MESSAGE
        elif category == "bedrock":
            commands_message = BEDROCK_COMMANDS_MESSAGE
        elif category == "java":
            commands_message = JAVA_COMMANDS_MESSAGE
        return commands_message

    async def _cmd_adduser(self, user_name: str, user_id: str, *args) -> str:
        """
        Add a user to the server's allowlist.json file.
        Better to use `whitelist` command instead of this.
        """
        if self.server_type == "bedrock":
            id_name = "xuid"
        elif self.server_type == "java":
            id_name = "uuid"
        allowlist = json.loads(self.allowlist_file.read_text())
        if any(
            (i["name"] == user_name or i.get(id_name) == user_id)
            for i in allowlist
        ):
            return "New user appears to be a duplicate user."
        new_entry = {
            "ignoresPlayerLimit": False,
            "name": user_name,
            id_name: user_id,
        }
        if self.server_type == "java":
            new_entry.pop("ignoresPlayerLimit")
        allowlist.append(new_entry)
        self.allowlist_file.write_text(json.dumps(allowlist))
        return f"Added user {user_name} to allowlist."

    async def _cmd_rmuser(self, user_name: str, *args) -> str:
        """Remove a user from the server's allowlist.json file."""
        allowlist = json.loads(self.allowlist_file.read_text())
        if not any(i["name"] == user_name for i in allowlist):
            return f"User *\"{user_name}\"* does not appear in allowlist."
        good_entries = [i for i in allowlist if i["name"] != user_name]
        self.allowlist_file.write_text(json.dumps(good_entries))
        return f"Removed user {user_name} from allowlist."

    async def _cmd_userrole(self, *args) -> str:
        return "Not yet implemented."

    async def _cmd_changeprop(self, *args) -> str:
        return "Not yet implemented."

    async def _cmd_showsettings(self, target_file: str, *args) -> str:
        if target_file == "allowlist" or target_file == "whitelist":
            file_path = self.allowlist_file
        elif target_file == "permissions":
            file_path = self.server_path / "permissions.json"
        elif target_file == "properties":
            file_path = self.server_path / "server.properties"
        else:
            return f"Unrecognised file identifier, *\"{target_file}\"*."
        file_contents = file_path.read_text()
        return f"**{file_path.name}**\n```{file_contents}```"

    async def _cmd_startserver(self, *args) -> str:
        """Launch and assign the server process."""
        if await self.server_running:
            return "The server is already running."
        if self.server_type == "bedrock":
            server_cmd = [self.server_cmd]
        elif self.server_type == "java":
            server_cmd = self.server_cmd.split(" ")
        self.server_proc = (
            await asyncio.subprocess.create_subprocess_exec(
                *server_cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                cwd=self.server_path,
                env=self.env,
            )
        )
        return "Started Minecraft server."

    async def _cmd_stopserver(self, *args) -> str:
        """
        Gracefully stop the server by sending the `/stop` command.
        This command is mostly just for consistency since sending `/stop`
        does the same thing.
        """
        if not await self.server_running:
            return "The server is already shutdown."
        await self.send_server_command("stop")
        return "Shutdown Minecraft server gracefully."

    async def _cmd_killserver(self, *args) -> str:
        """Force stop the server process."""
        try:
            self.server_proc.kill()
        except Exception:
            pass
        return "Shutdown Minecraft server forcefully."

    async def send_server_command(
        self,
        command: str,
        user_name: str = "unknown",
    ) -> None:
        """
        Send a server command. This command does not return a message
        as some commands sent to the server need no confirmation (e.g. `/say`),
        however, if the server does give some reply, it'll be picked up and
        enqueued in the `CraftCommander.poll_server_messages`.
        """
        if not await self.server_running:
            return "The server isn't running."
        # Append the Discord username to the "say" command.
        if command.startswith("say"):
            command = f'say ({user_name}@Discord){command[3:]}'
        encoded_command = bytes(command, encoding="utf-8") + b"\n"
        self.server_proc.stdin.write(encoded_command)

    async def poll_server_messages(self) -> None:
        """Poll the server's output and enqueue any new messages."""
        while True:
            LOGGER.debug("Polling for server messages...")
            await asyncio.sleep(1)
            if not await self.server_running:
                continue
            # All stdout.<read> methods will hang waiting for an EOF so
            # using a loop to grab everythign available and then letting
            # it hang while nothing is being sent.
            while True:
                try:
                    buffer = await self.server_proc.stdout.readuntil(self.eol)
                except asyncio.exceptions.IncompleteReadError:
                    break
                # Skip spammy messages.
                if not any(
                    re.search(pattern, str(buffer))
                    for pattern in IGNORED_MESSAGE_PATTERNS
                ):
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
                f" Run `{CMD_PREFIX}listcommands` to list commands."
            )
        elif base_command in BEDROCK_COMMAND_NAMES + JAVA_COMMAND_NAMES:
            if not await self.server_running:
                message = (
                    f"Server not running... start it with the"
                    f" `{CMD_PREFIX}startserver` command and try again."
                )
            else:
                message = await self.send_server_command(command, user_name)
        else:
            command_method = getattr(self, f"_cmd_{base_command}")
            try:
                message = await command_method(*command_args)
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
