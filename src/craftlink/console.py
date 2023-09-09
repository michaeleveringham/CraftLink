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
        "--bedrock-server-install-directory",
        default=os.environ.get("BEDROCK_SERVER_INSTALL_DIRECTORY", ""),
        dest="server_dir",
        help="Directory that the Bedrock server executable is in.",
    )
    options = parser.parse_args()
    try:
        asyncio.run(amain(options))
    except KeyboardInterrupt:
        pass
    LOGGER.info("Processes exited successfully, quitting.")
