import asyncio
import discord
from discord.ext import commands
from mcstatus import JavaServer
import os

# Get server

SERVER_IP = os.getenv("MINECRAFT_SERVER_IP")
if not SERVER_IP:
    raise RuntimeError("DISCORD_GUILD_ID is missing from your .env file")

minecraftServer = JavaServer.lookup(SERVER_IP)

# Commands

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Server IP
    @discord.app_commands.command(
        name="ip",
        description="Shows the IP adress of the minecraft server."
    )
    async def getIP(self, interaction: discord.Interaction):
        await interaction.response.send_message(
                f"The server is using Minecraft version: {SERVER_IP}."
        )

    # Check status
    @discord.app_commands.command(
        name="status",
        description="Pings the minecraft server to check the status."
    )
    async def getStatus(self, interaction: discord.Interaction):
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
        name="version",
        description="Shows the version of minecraft the server is running on."
    )
    async def getVersion(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            status = await asyncio.to_thread(minecraftServer.status)
            await interaction.followup.send(
                f"The server is using Minecraft version: {status.version.name}."
            )

        except (TimeoutError, OSError):
            await interaction.followup.send(
                "Server is offline or unreachable."
            )

async def setup(bot):
    await bot.add_cog(Commands(bot))