import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Set .env variables

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from your .env file")

GUILD_ID = os.getenv("DISCORD_GUILD_ID")
if not GUILD_ID:
    raise RuntimeError("DISCORD_GUILD_ID is missing from your .env file")

# Initialize bot

class MyBot(commands.Bot):

    async def setup_hook(self):
        await self.load_extension("cogs.commands")

        guild = discord.Object(id=int(GUILD_ID))
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

intents = discord.Intents.default()
bot = MyBot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)