CMD_PREFIX = "!"


def commands_message(command_names: tuple[str], server_type: str) -> str:
    server_commands = "\n- ".join(
        [f"`{CMD_PREFIX}{i}`" for i in command_names]
    )
    return f"**{server_type} Server Commands**\n- {server_commands}"


# Administrative or maintenance commands, usually outside server context.
ADMIN_COMMANDS = {
    "adduser": {
        "help": (
            "Add a user to the server's allowlist."
            " It's recommended to instead use the server-level"
            " command for allowlist control, it does not require a (x/u)uid."
        ),
        "args": "user_name user_xuid_or_uuid",
    },
    "changeprop": {
        "help": "Change a server property (server.properties).",
        "args": "property_name property_value",
    },
    "killserver": {
        "help": "Force shutdown the Minecraft server.",
        "args": "",
    },
    "listcommands": {
        "help": "Lists commands accepted by this bot.",
        "args": "[type (\"admin\", \"bedrock\", \"java\")]",
    },
    "rmuser": {
        "help": "Remove a user from the server's allowlist.",
        "args": "user_name",
    },
    "showsettings": {
        "help": "View a server settings file.",
        "args": "[file (\"allowlist\", \"permissions\", \"properties\")]",
    },
    "startserver": {
        "help": "Start the Minecraft server.",
        "args": "",
    },
    "stopserver": {
        "help": "Gracefully shutdown the Minecraft server.",
        "args": "",
    },
    "userrole": {
        "help": "Change user permissions (permissions.json).",
        "args": "user_xuid permission_name",
    },
}

ADMIN_COMMAND_NAMES = tuple(ADMIN_COMMANDS.keys())

# Bedrock commands names, will have no corresponding method.
# No help or details for these, users can use the help command for that.
BEDROCK_COMMAND_NAMES = (
    "?",
    "allowlist",
    "alwaysday",
    "camerashake",
    "changesetting",
    "clear",
    "clearspawnpoint",
    "clone",
    "connect",
    "damage",
    "daylock",
    "deop",
    "dialogue",
    "difficulty",
    "effect",
    "enchant",
    "event",
    "execute",
    "fill",
    "fog",
    "function",
    "gamemode",
    "gamerule",
    "gametest",
    "give",
    "help",
    "inputpermission",
    "kick",
    "kill",
    "list",
    "locate",
    "loot",
    "me",
    "mobevent",
    "msg",
    "music",
    "op",
    "ops",
    "particle",
    "permission",
    "playanimation",
    "playsound",
    "reload",
    "reloadconfig",
    "replaceitem",
    "ride",
    "save",
    "say",
    "schedule",
    "scoreboard",
    "script",
    "setblock",
    "setmaxplayers",
    "setworldspawn",
    "spawnpoint",
    "spreadplayers",
    "stop",
    "stopsound",
    "structure",
    "summon",
    "tag",
    "teleport",
    "tell",
    "tellraw",
    "testfor",
    "testforblock",
    "testforblocks",
    "tickingarea",
    "time",
    "title",
    "titleraw",
    "toggledownfall",
    "tp",
    "w",
    "weather",
    "whitelist",
    "wsserver",
    "xp",
)

# Again, no details for command names, users can use help command.
JAVA_COMMAND_NAMES = (
    "advancement",
    "attribute",
    "execute",
    "bossbar",
    "clear",
    "clone",
    "damage",
    "data",
    "datapack",
    "debug",
    "defaultgamemode",
    "difficulty",
    "effect",
    "me",
    "enchant",
    "experience",
    "xp",
    "fill",
    "fillbiome",
    "forceload",
    "function",
    "gamemode",
    "gamerule",
    "give",
    "help",
    "item",
    "kick",
    "kill",
    "list",
    "locate",
    "loot",
    "msg",
    "tell",
    "w",
    "particle",
    "place",
    "playsound",
    "reload",
    "recipe",
    "return",
    "ride",
    "say",
    "schedule",
    "scoreboard",
    "seed",
    "setblock",
    "spawnpoint",
    "setworldspawn",
    "spectate",
    "spreadplayers",
    "stopsound",
    "summon",
    "tag",
    "team",
    "teammsg",
    "tm",
    "teleport",
    "tp",
    "tellraw",
    "time",
    "title",
    "trigger",
    "weather",
    "worldborder",
    "jfr",
    "ban-ip",
    "banlist",
    "ban",
    "deop",
    "op",
    "pardon",
    "pardon-ip",
    "perf",
    "save-all",
    "save-off",
    "save-on",
    "setidletimeout",
    "stop",
    "whitelist",
)

ALL_COMMAND_NAMES = [
    *ADMIN_COMMAND_NAMES,
    *BEDROCK_COMMAND_NAMES,
    *JAVA_COMMAND_NAMES,
]

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
ADMIN_COMMANDS_MESSAGE = f"**Administrative Commands** \n{admin_commands}"

BEDROCK_COMMANDS_MESSAGE = commands_message(BEDROCK_COMMAND_NAMES, "Bedrock")
JAVA_COMMANDS_MESSAGE = commands_message(JAVA_COMMAND_NAMES, "Java")
