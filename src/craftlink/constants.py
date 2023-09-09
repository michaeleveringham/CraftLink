CMD_PREFIX = "!"

# Administrative or maintenance commands, usually outside server context.
ADMIN_COMMANDS = {
    "adduser": {
        "help": "Add a user to the server's allowlist.",
        "args": "user_name user_xuid",
    },
    "changeprop": {
        "help": "Change a server property (server.properties).",
        "args": "property_name property_value",
    },
    "killserver": {
        "help": "Force shutdown the Bedrock server.",
        "args": "",
    },
    "listcommands": {
        "help": "Lists commands accepted by this bot.",
        "args": "[type (\"admin\", \"server\")]",
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
        "help": "Start the Bedrock server.",
        "args": "",
    },
    "stopserver": {
        "help": "Gracefully shutdown the Bedrock server.",
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

ALL_COMMAND_NAMES = [
    *ADMIN_COMMAND_NAMES,
    *BEDROCK_COMMAND_NAMES,
]
