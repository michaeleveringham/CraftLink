from __future__ import annotations
import asyncio
import io
import logging
from collections import deque
from pathlib import Path

import discord

from craftlink.command import CraftCommander
from craftlink.constants import CMD_PREFIX


LOGGER = logging.getLogger(__name__)


class CraftBot(discord.Client):
    def __init__(
        self, token: str,
        server_dir: str,
        channel_id: str,
        server_type: str,
        java_mem_range: tuple[int],
        use_box64: bool,
    ) -> None:
        self.token = token
        self.server_type = server_type
        server_path = Path(server_dir)
        self.server_message_queue = deque([])
        self.commander = CraftCommander(
            server_path,
            self.server_message_queue,
            server_type,
            java_mem_range,
            use_box64,
        )
        self.channel_id = int(channel_id)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        super().__init__(intents=intents)

    async def __aenter__(self, *args, **kwargs) -> CraftBot:
        """Spawn tasks to handle the message queue upon context entry."""
        asyncio.create_task(self.commander.poll_server_messages())
        asyncio.create_task(self.process_server_message_queue())
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """Kill the server on context exit."""
        await self.stop()

    async def run(self) -> None:
        """
        Run the server.
        Using `discord.Client.start` here as already within the running loop.
        """
        LOGGER.info("Starting Discord bot...")
        await self.start(self.token)

    async def stop(self) -> None:
        """Stop the server, gracefully at first, then forcefully if needed."""
        if await self.commander.server_running:
            self.commander._cmd_stopserver(None)
        LOGGER.info("Waiting a few seconds for server to stop gracefully...")
        await asyncio.sleep(5)
        try:
            if await self.commander.server_running:
                LOGGER.warning("Server did not stop, killing it.")
                self.commander._cmd_killserver(None)
        except Exception:
            pass

    async def say(self, message: str) -> None:
        """Send a message to the channel. Send large messages as txt files."""
        if len(message) <= 2000:
            await self.channel.send(message)
        else:
            message_io = io.StringIO(message)
            attachment = discord.File(message_io, filename="attachment.txt")
            await self.channel.send(file=attachment)

    async def process_server_message_queue(self) -> None:
        """Send queued server messages to the Discord channel."""
        while True:
            message = ""
            while self.server_message_queue:
                message += self.server_message_queue.popleft().decode()
            if message:
                # Drop the last newline from the messages.
                message = message[:-1]
                # Send large messages as attachments,
                footer = f"Messages from {self.server_type.title()} server."
                if len(message) > 4000:
                    message = f"{footer}\n{message}"
                    await self.say(message)
                else:
                    # Send messages as embeds when possible for cleaner look.
                    embed = discord.Embed(description=f"```{message}```")
                    embed.set_footer(text=footer)
                    await self.channel.send(embed=embed)
            await asyncio.sleep(2)

    async def on_ready(self) -> None:
        self.channel = await self.fetch_channel(self.channel_id)
        LOGGER.info(f"{self.user.name} is now running.")

    async def on_message(self, message: discord.Message) -> None:
        """Messages starting with prefix are parsed and dispatched."""
        if message.author == self.user or message.channel.id != self.channel_id:
            return
        user_name = message.author.name
        text = message.content
        if not text.startswith(CMD_PREFIX):
            return
        else:
            command = text[1:]
            LOGGER.info(f"Processing command from user {user_name}, {command}")
            response = await self.commander.dispatch_command(command, user_name)
            if response:
                await self.say(response)
