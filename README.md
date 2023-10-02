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

### Dependencies

Requires Python 3.9+.

Install via `pip install craftlink`.

Or, clone and run `poetry install` to install from source.

You'll need to download [the Bedrock Server](https://www.minecraft.net/en-us/download/server/bedrock),
or [the Java server](https://www.minecraft.net/en-us/download/server).

You'll *probably* want to run your server manually first to configure your world. You can migrate an
existing local world to be a server pretty easily by copying the world data into
`<server_directory>/worlds` (Bedrock), or replacing the `<server_directory>/world` folder (Java).

### Operating System

Currently supports Windows and Linux (tested on Debian). 

Likely works on MacOS, but not yet tested.

## Running

To run locally, just invoke `craftlink` with the necesary arguments/environment variables set.

Required arguments:

- `-t`, `--discord-bot-token`, `DISCORD_BOT_TOKEN` - Token to use to authenticate the Discord bot.
- `-c`, `--discord-channel-id`, `DISCORD_CHANNEL_ID` - Discord channel ID to target the bot's messages to.
- `-d`, `--server-install-directory`, `SERVER_INSTALL_DIRECTORY` - Directory that the server executable is in.

Optional arguments:

- `-y`, `--server-type`, `SERVER_TYPE` - Type of server to be run ("bedrock" or "java"), defaults to bedrock.
- `-m`, `--java-memory-min`, `JAVA_MEMORY_MIN` - (Java only) minimum server memory to allocate, defaults to 1024.
- `-x`, `--java-memory-max`, `JAVA_MEMORY_MAX` - (Java only) maximum server memory to allocate, defaults to 1024.
- `-is-arm64`, `IS_ARM64` - Flag to indicate running on arm64 architecture.

### ARM64 and Bedrock

You must use the switch `--isarm-64` and set the environment variable `IS_ARM64`
so the command is dispatched correctly.

The Bedrock binary is meant for x86_64 architecture; to get it to run
on arm64 devices, [`box64`](https://github.com/ptitSeb/box64) emulation is used.

If building the Bedrock Docker image, specify `--platform=linux/arm64` and
`box64` will be installed automatically.

Otherwise, ensure your system has `box64` installed and available in the `PATH`.

(Shoutout to [this issue comment](https://github.com/itzg/docker-minecraft-bedrock-server/issues/140#issuecomment-1126406059)
from [`docker-minecraft-bedrock-server`](https://github.com/itzg/docker-minecraft-bedrock-server)
for pointing me in the right direction here.)

### Docker

To run in a Docker container, you'll need to ensure your `.env` file is populated first.
Copy `.env.template` and fill in the blanks.
Ensure that `SERVER_INSTALL_DIRECTORY` is the directory to your local server files, not
the directory in the Docker image.

By default this image will mount existing server files from the host machine to the container.
Note that for Bedrock, you only need to have the below files and folders, you don't need the executable/binary. 
- `allowlist.json`
- `permissions.json`
- `server.properties`
- `worlds`

For Java, the entire directory will be mounted.

Regardless of server type, ensure you run the world locally once before mounting it.

When ready, run `docker compose up <server_type: java or bedrock>` to run.

## Improvements

- Add tests.
- Add user roles at the bot level to restrict certain actions.
  - Could be multiple roles such that "admins" have all perms, "mods" have less, and "users" have none or just `/say`.
- Support for modded server launchers.

## Affiliate Disclaimer

In no way affiliated with Microsoft or Mojang (that'd be dope though, feel free to reach out, folks).
