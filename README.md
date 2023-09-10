# CraftLink

A Discord bot to control a Minecraft server remotely.

## Examples

### Starting, Stopping, Sending Commands (Bedrock and Java)
![Starting and getting help from Bedrock server via Discord.](https://github.com/michaeleveringham/CraftLink/blob/main/images/bedrock-server-examples.png)

![Getting help and stopping Java server via Discord](https://github.com/michaeleveringham/CraftLink/blob/main/images/java-server-examples.png)

### Command `/say` from In-Game POV
![Sending a message from Discord to Minecraft.](https://github.com/michaeleveringham/CraftLink/blob/main/images/discord-chat-to-game.jpg)

## Security Disclaimer

While there is some validation around the commands sent to the server, it is important to note that
it is likely not secure. 

**It is very possible that this could be abused to send and execute malicious code!**

## Recommended Restrictions

Since this connection gives full control over a Minecraft server and it's various properties
and settings, the bot requires and is limited to a single Discord channel within a
Discord server.

It is recommended this channel be private and limited to only server admins and moderators.

Granular permissions based on Discord role may come eventually...!

## Setup

### Operating System

Currently Windows only simply because that's where my server is living... but planning to bring to Linux, too!

### Dependencies

Requires Python 3.9+.

Install via `pip install craftlink`.

Or, clone and run `poetry install` to install from source.

You'll need to download [the Bedrock Server](https://www.minecraft.net/en-us/download/server/bedrock),
or [the Java server](https://www.minecraft.net/en-us/download/server).

You'll *probably* want to run your server manually first to configure your world. You can migrate an
existing local world to be a server pretty easily by copying the world data into
`<server_directory>/worlds` (Bedrock), or replacing the `<server_directory>/world` folder (Java).

## Running

To run the server, just invoke `craftlink` with the necesary arguments/environment variables set.

Required arguments:

- `-t`, `--discord-bot-token`, `DISCORD_BOT_TOKEN` - Token to use to authenticate the Discord bot.
- `-c`, `--discord-channel-id`, `DISCORD_CHANNEL_ID` - Discord channel ID to target the bot's messages to.
- `-d`, `--server-install-directory`, `SERVER_INSTALL_DIRECTORY` - Directory that the server executable is in.
- `-y`, `--server-type`, `SERVER_TYPE` - Type of server to be run ("bedrock" or "java"), defaults to bedrock.
- `-m`, `--java-memory-min`, `JAVA_MEMORY_MIN` - (Java only) minimum server memory to allocate, defaults to 1024.
- `-x`, `--java-memory-max`, `JAVA_MEMORY_MAX` - (Java only) maximum server memory to allocate, defaults to 1024.

## Improvements

- Add tests.
- Add user roles at the bot level to restrict certain actions.
  - Could be multiple roles such that "admins" have all perms, "mods" have less, and "users" have none or just `/say`.
- Be cool if this could run in a container altogether.
- Support for modded server launchers.

## Affiliate Disclaimer

In no way affiliated with Microsoft or Mojang (that'd be dope though, feel free to reach out, folks).
