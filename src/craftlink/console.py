import asyncio
import logging
import os
from argparse import ArgumentParser

from dotenv import load_dotenv

from craftlink.bot import CraftBot


load_dotenv()

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


async def amain(options):
    async with CraftBot(
        token=options.token,
        server_dir=options.server_dir,
        channel_id=options.channel_id,
        server_type=options.server_type,
        java_mem_range=(options.java_memory_min, options.java_memory_max),
    ) as bot:
        await bot.run()


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-t",
        "--discord-bot-token",
        default=os.environ.get("DISCORD_BOT_TOKEN", ""),
        dest="token",
        help="Token to use to authenticate the Discord bot.",
    )
    parser.add_argument(
        "-c",
        "--discord-channel-id",
        default=os.environ.get("DISCORD_CHANNEL_ID", ""),
        dest="channel_id",
        help="Discord channel ID to target the bot's messages to.",
    )
    parser.add_argument(
        "-d",
        "--server-install-directory",
        default=os.environ.get("SERVER_INSTALL_DIRECTORY", ""),
        dest="server_dir",
        help="Directory that the server executable is in.",
    )
    parser.add_argument(
        "-y",
        "--server-type",
        default=os.environ.get("SERVER_TYPE", "bedrock"),
        choices=["bedrock", "java"],
        required=False,
        help="Type of server to be run (bedrock or java), defaults to bedrock.",
    )
    parser.add_argument(
        "-m",
        "--java-memory-min",
        default=os.environ.get("JAVA_MEMORY_MIN", "1024"),
        type=int,
        required=False,
        help="(Java only) minimum server memory to allocate, defaults to 1024.",
    )
    parser.add_argument(
        "-x",
        "--java-memory-max",
        default=os.environ.get("JAVA_MEMORY_MAX", "1024"),
        type=int,
        required=False,
        help="(Java only) maximum server memory to allocate, defaults to 1024.",
    )
    options = parser.parse_args()
    try:
        asyncio.run(amain(options))
    except KeyboardInterrupt:
        pass
    LOGGER.info("Processes exited successfully, quitting.")
