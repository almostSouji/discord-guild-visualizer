#!/usr/bin/env python3

import json

guild_path = "./guild.json"
channels_path = "./channels.json"


# ---------------

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"  # orange on some systems
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
LIGHT_GRAY = "\033[37m"
DARK_GRAY = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
WHITE = "\033[97m"

RESET = "\033[0m"  # called to return to standard terminal text color

# ---------------

CHANNEL_TYPES = [
    "guild_text",
    "dm",
    "guild_voice",
    "group_dm",
    "guild_category",
    "guild_announcement",
    None,
    None,
    None,
    None,
    "announcement_thread",
    "public_thread",
    "private_thread",
    "guild_stage_voice",
    "guild_directory",
    "guild_forum",
    "guild_media",
]

CHANNEL_INDICATORS = [
    "T",
    "DM",
    "V",
    "G",
    "C",
    "A",
    None,
    None,
    None,
    None,
    "TAn",
    "TPu",
    "TPr",
    "S",
    "D",
    "F",
    "M",
]

PERMISSIONS = [
    ("CREATE_INSTANT_INVITE", 1 << 0),
    ("KICK_MEMBERS", 1 << 1),
    ("BAN_MEMBERS", 1 << 2),
    ("ADMINISTRATOR", 1 << 3),
    ("MANAGE_CHANNELS", 1 << 4),
    ("MANAGE_GUILD", 1 << 5),
    ("ADD_REACTIONS", 1 << 6),
    ("VIEW_AUDIT_LOG", 1 << 7),
    ("PRIORITY_SPEAKER", 1 << 8),
    ("STREAM", 1 << 9),
    ("VIEW_CHANNEL", 1 << 10),
    ("SEND_MESSAGES", 1 << 11),
    ("SEND_TTS_MESSAGES", 1 << 12),
    ("MANAGE_MESSAGES", 1 << 13),
    ("EMBED_LINKS", 1 << 14),
    ("ATTACH_FILES", 1 << 15),
    ("READ_MESSAGE_HISTORY", 1 << 16),
    ("MENTION_EVERYONE", 1 << 17),
    ("USE_EXTERNAL_EMOJIS", 1 << 18),
    ("VIEW_GUILD_INSIGHTS", 1 << 19),
    ("CONNECT", 1 << 20),
    ("SPEAK", 1 << 21),
    ("MUTE_MEMBERS", 1 << 22),
    ("DEAFEN_MEMBERS", 1 << 23),
    ("MOVE_MEMBERS", 1 << 24),
    ("USE_VAD", 1 << 25),
    ("CHANGE_NICKNAME", 1 << 26),
    ("MANAGE_NICKNAMES", 1 << 27),
    ("MANAGE_ROLES", 1 << 28),
    ("MANAGE_WEBHOOKS", 1 << 29),
    ("MANAGE_GUILD_EXPRESSIONS", 1 << 30),
    ("USE_APPLICATION_COMMANDS", 1 << 31),
    ("REQUEST_TO_SPEAK", 1 << 32),
    ("MANAGE_EVENTS", 1 << 33),
    ("MANAGE_THREADS", 1 << 34),
    ("CREATE_PUBLIC_THREADS", 1 << 35),
    ("CREATE_PRIVATE_THREADS", 1 << 36),
    ("USE_EXTERNAL_STICKERS", 1 << 37),
    ("SEND_MESSAGES_IN_THREADS", 1 << 38),
    ("USE_EMBEDDED_ACTIVITIES", 1 << 39),
    ("MODERATE_MEMBERS", 1 << 40),
    ("VIEW_CREATOR_MONETIZATION_ANALYTICS", 1 << 41),
    ("USE_SOUNDBOARD", 1 << 42),
    ("CREATE_GUILD_EXPRESSIONS", 1 << 43),
    ("CREATE_EVENTS", 1 << 44),
    ("USE_EXTERNAL_SOUNDS", 1 << 45),
    ("SEND_VOICE_MESSAGES", 1 << 46),
    ("SEND_POLLS", 1 << 49),
    ("USE_EXTERNAL_APPS", 1 << 50),
]

MOD_PERMISSIONS = (
    1 << 1
    | 1 << 2
    | 1 << 3
    | 1 << 4
    | 1 << 5
    | 1 << 13
    | 1 << 28
    | 1 << 29
    | 1 << 30
    | 1 << 34
    | 1 << 40
    | 1 << 41
)

assert len(CHANNEL_TYPES) == len(
    CHANNEL_INDICATORS
), "Every channel type should have an indicator"


with open(guild_path) as guild_file:
    guild = json.loads(guild_file.read())

with open(channels_path) as channels_file:
    channels_data = json.loads(channels_file.read())

roles = dict()

for role in guild["roles"]:
    roles[role["id"]] = role

channels = dict()
relations = dict()
categories = []
root = []

for channel in channels_data:
    channels[channel["id"]] = channel

    if channel["type"] == 4:  # category
        categories.append(channel["id"])
        continue

    parent_id = channel["parent_id"]
    if parent_id:
        siblings = relations.get(parent_id, [])
        siblings.append(channel["id"])
        relations[parent_id] = siblings
        continue

    root.append(channel["id"])


def elevated_permission_mark(flag):
    return f"{YELLOW} [2FA]{RESET}" if flag & MOD_PERMISSIONS != 0 else ""


H2 = f"{DARK_GRAY}---{RESET}"
H1 = f"{DARK_GRAY}==={RESET}"

print(f"{H1} {guild["name"]} {DARK_GRAY}({guild["id"]}) {H1}")
print(f"{H2} Roles {H2}")
print()

for role_id, role in roles.items():
    print(
        f"{DARK_GRAY}•{RESET} {role["name"]} {DARK_GRAY}({role_id}) {BRIGHT_BLUE}{role.get("permissions", "0")}{RESET}"
    )

    permissions = []
    for name, flag in PERMISSIONS:
        if int(role["permissions"]) & flag == flag:
            permissions.append(f"{BRIGHT_BLUE}{name}{elevated_permission_mark(flag)}")

    if len(permissions):
        print(f"   {'\n   '.join(permissions)}")

print()


def render_overwrites(channel, space=0):
    overwrites = channel["permission_overwrites"]
    for overwrite in sorted(
        overwrites, key=lambda x: (x["id"] != guild["id"], x["type"] == 1)
    ):
        overwrite_type = "U" if overwrite["type"] == 1 else "R"
        name = roles.get(overwrite["id"], {}).get("name", "")
        name = name if name.startswith("@") else f"@{name}"

        if overwrite["type"] == 1:
            name = "<user>"

        target = f"{name} {DARK_GRAY}({overwrite["id"]})"

        print(
            f"{space * " "}{DARK_GRAY}{overwrite_type}{RESET} {target} {DARK_GRAY}| {BRIGHT_GREEN}+{overwrite.get("allow", "0")} {DARK_GRAY}| {BRIGHT_RED}-{overwrite.get("deny", "0")}{RESET}"
        )

        allowed = []
        denied = []

        for name, flag in PERMISSIONS:
            mark = elevated_permission_mark(flag)
            if int(overwrite["allow"]) & flag == flag:
                allowed.append(f"{name}{mark}")
            if int(overwrite["deny"]) & flag == flag:
                denied.append(f"{name}{mark}")

        for line in denied:
            print(f"{(space + 3) * " "}{RED}- {line}{RESET}")

        for line in allowed:
            print(f"{(space + 3) * " "}{GREEN}+ {line}{RESET}")


for category_id in categories:
    channel = channels.get(category_id, dict())

    print(f"{H2} {channel["name"]} {DARK_GRAY}({category_id}) {H2}")
    render_overwrites(channel, 4)
    print()

    for child_id in relations.get(category_id, []):
        child = channels.get(child_id, None)
        if not child:
            continue

        type_indicator = CHANNEL_INDICATORS[child["type"]]
        description = child.get("topic", None)
        mark = "#" if type_indicator == "T" else ""
        print(
            f"{DARK_GRAY}• {type_indicator} {RESET}{mark}{child["name"]} {DARK_GRAY}({child_id}){RESET}"
        )

        if description:
            for line in description.split("\n"):
                print(f"{" " * 4}{LIGHT_GRAY}| {line}{RESET}")
            print()

        render_overwrites(child, 4)
    print()

for root_id in root:
    channel = channels.get(root_id, dict())
    type_indicator = CHANNEL_INDICATORS[channel["type"]]
    print(f"{type_indicator} {channel["name"]} ({root_id})")
