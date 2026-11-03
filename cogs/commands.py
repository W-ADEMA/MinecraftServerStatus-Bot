import asyncio
import discord
from discord.ext import commands
from mcstatus import JavaServer
import os

SERVER_IP = os.getenv("MINECRAFT_SERVER_IP")

minecraftServer = JavaServer(SERVER_IP, 21289, timeout=10)

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Check status
    @discord.app_commands.command(
        name="check-status",
        description="Pings the minecraft server to check the status."
    )
    async def checkStatus(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            status = await asyncio.to_thread(minecraftServer.status)
            await interaction.followup.send(
                f"Server is online! ({round(status.latency)} ms)"
            )

        except (TimeoutError, OSError):
            await interaction.followup.send(
                "Server is offline or unreachable."
            )

    # Check Minecraft version
    @discord.app_commands.command(
        name="check-version",
        description="Shows the version of minecraft the server is running on."
    )
    async def checkStatus(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            status = await asyncio.to_thread(minecraftServer.status)
            await interaction.followup.send(
                f"The server is using Minecraft version {status.version.name}."
            )

        except (TimeoutError, OSError):
            await interaction.followup.send(
                "Server is offline or unreachable."
            )

async def setup(bot):
    await bot.add_cog(Commands(bot))