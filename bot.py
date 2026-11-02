import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from mcstatus import JavaServer

# Set .env variables

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from your .env file")

GUILD_ID = os.getenv("DISCORD_GUILD_ID")
if not GUILD_ID:
    raise RuntimeError("DISCORD_GUILD_ID is missing from your .env file")

SERVER_IP = os.getenv("MINECRAFT_SERVER_IP")
if not SERVER_IP:
    raise RuntimeError("MINECRAFT_SERVER_IP is missing from your .env file")

# Initialize bot

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="", intents=intents)

minecraftServer = JavaServer(SERVER_IP, 21289, timeout=10)

# Slash commands

@bot.tree.command(
    name="check-status",
    description="Pings the minecraft server to check the status.",
    guild=discord.Object(id=GUILD_ID)
)
async def checkStatus(interaction):
    await interaction.response.defer()

    try:
        status = await asyncio.to_thread(minecraftServer.status)
        await interaction.followup.send(f"Server is online! ({round(status.latency)} ms)")

    except (TimeoutError, OSError):
        await interaction.followup.send("Server is offline or unreachable.")


@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)