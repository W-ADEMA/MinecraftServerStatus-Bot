import os
import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
from dotenv import load_dotenv
import asyncio

load_dotenv()

CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
SERVER_IP = os.getenv("MINECRAFT_SERVER_IP")

class Monitor(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status_message = None
        self.my_task.start()

    def cog_unload(self):
        self.my_task.cancel()

    @tasks.loop(minutes=1)
    async def my_task(self):
        discordChannel = await self.bot.fetch_channel(CHANNEL_ID)

        # Creates playerlist
        try:
            minecraftServer = JavaServer.lookup(SERVER_IP)
            status = await asyncio.to_thread(minecraftServer.status)
            players = status.players.sample

            if players:
                playerListOutput = (
                    "**Players online:**\n" +
                    "\n".join(discord.utils.escape_markdown(player.name) for player in players)
                )
            else:
                if status.players.online > 0:
                    playerListOutput = "Server does not expose playerlist"
                else:
                    playerListOutput = "No players online"

            messageContent = (
                f"Players: `{status.players.online}/{status.players.max}`\n"
                "\n"
                f"{playerListOutput}"
            )

        except (TimeoutError, OSError):
            messageContent = (
                "Server is offline or unreachable"
            )

        # Checks if message can be edited or needs to be sent
        if self.status_message is None:
            self.status_message = await discordChannel.send(messageContent)
        else:
            try:
                await self.status_message.edit(content=messageContent)
            except discord.NotFound:
                self.status_message = await discordChannel.send(messageContent)

    @my_task.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

        # Delete old playerlist(s)
        discordChannel = await self.bot.fetch_channel(CHANNEL_ID)
        async for message in discordChannel.history(limit=None):
            if message.author == self.bot.user:
                await message.delete()

async def setup(bot):
    if not CHANNEL_ID:
        print("DISCORD_CHANNEL_ID is missing from .env file, skipping playerlistChannel Cog")
        return
    
    await bot.add_cog(Monitor(bot))