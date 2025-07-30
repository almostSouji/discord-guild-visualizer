# About

Visualize the layout and permission hierarchy for discord server data in raw API format.

# Usage

1. Put the guild payload (`GET /guilds/:id`) into `guild.json` in the project root
2. Put the channels payload (`GET /guilds/:id/channels`) into `channels.json` in the project root
3. Run the script `python ./visualize.py`

# Supported information

- Roles (permissions)
- Categories (child channels, permissions)
- Channels (type, permission overwrites and topic text)

> [!TIP]
> Yellow `[2FA]` marked permissions are considered "elevated", meaning they require 2FA to be configured for accounts making use of them.

> [!TIP]
> If you don't know how to interpret permission overwrites, check out the [discord developers documentation regarding permission and overwrite hierarchy](https://discord.com/developers/docs/topics/permissions#permission-hierarchy). Displaying all permissions after overwrites would be visually overwhelming, though i might add this as a switch later.

