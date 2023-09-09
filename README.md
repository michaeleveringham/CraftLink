# CraftLink

A Discord bot to control a Minecraft Bedrock server remotely.

## Examples

![Starting and stopping server via Discord.](https://github.com/michaeleveringham/CraftLink/blob/main/images/start-stop-server.png)

![Sending a message from Discord to Minecraft.](https://github.com/michaeleveringham/CraftLink/blob/main/images/discord-chat-to-game.jpg)

## Security Disclaimer

While there is some validation around the commands sent to the server, it is important to note that
it is not secure. 

**It is very likely that this could be abused to send and execute malicious code!**

## Setup

### Operating System

Currently Windows only simply because that's where my server is living... but planning to bring to Linux, too!

### Dependencies

Requires Python 3.9+.

Install via `pip install craftlink`.

Or, clone and run `poetry install` to install from source.

You'll need to [download the Bedrock Server](https://www.minecraft.net/en-us/download/server/bedrock).
You'll *probably* want to run this manually first to configure your world. You can migrate an
existing local bedrock world to be a Bedrock server pretty easily by copying the world data into
`<server_directory>/worlds`.

## Running

To run the server, just invoke `craftlink` with the necesary arguments/environment variables set.

Required arguments:

- `-t`, `--discord-bot-token`, `DISCORD_BOT_TOKEN` - Token to use to authenticate the Discord bot.
- `-c`, `--discord-channel-id`, `DISCORD_CHANNEL_ID` - Discord channel ID to target the bot's messages to.
- `-d`, `--bedrock-server-install-directory`, `BEDROCK_SERVER_INSTALL_DIRECTORY` - Directory that the Bedrock server executable is in.

## Improvements

- Add tests.
- Add user roles at the bot level to restrict certain actions.
  - Could be multiple roles such that "admins" have all perms, "mods" have less, and "users" have none or just `/say`.
- Be cool if this could run in a container altogether.

## Affiliate Disclaimer

In no way affiliated with Microsoft or Mojang (that'd be dope though, feel free to reach out, folks).
