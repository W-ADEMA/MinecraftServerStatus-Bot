# MinecraftServerStatus-Bot
 
A Discord bot that displays the status of a Minecraft (Java Edition) server. 
 
## Features
 
- **Slash commands** that can be used to get info about the server
- **Live player list channel** (optional): a single message that is edited every minute with the current player count and names

## Setup
 
Create a `.env` file in the project root:
 
```env
DISCORD_TOKEN=your-bot-token
DISCORD_GUILD_ID=your-discord-server-id
MINECRAFT_SERVER_IP=play.example.com
 
# optional
DISCORD_CHANNEL_ID=your-channel-id
```

## Live player list channel
 
If `DISCORD_CHANNEL_ID` is set, the bot posts one message in that channel and edits it every minute with the current player count and names.
 
**Important:** on startup the bot **deletes all of its own previous messages** in that specific channel so there is only ever one status message. Use a dedicated channel for it, and consider making it read-only for members.

## Slash commands
 
| Command       | Description                                                       |
| ------------- | ----------------------------------------------------------------- |
| `/ip`         | Shows the IP address of the Minecraft server                      |
| `/status`     | Pings the server and reports whether it is online   |
| `/version`    | Shows the Minecraft version the server is running                 |
| `/playerlist` | Shows the number of players online and their names                |

## Requirements
 
- Python 3.13 or newer
- Dependencies (see `requirements.txt`)
- A Discord bot application and token
- A Minecraft **Java Edition** server