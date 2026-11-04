import asyncio
import discord
from discord.ext import commands
from mcstatus import JavaServer
import os

# Get server

SERVER_IP = os.getenv("MINECRAFT_SERVER_IP")

minecraftServer = JavaServer.lookup(SERVER_IP)

# Commands

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Server IP
    @discord.app_commands.command(
        name="ip",
        description="Shows the IP adress of the minecraft server"
    )
    async def getIP(self, interaction: discord.Interaction):
        await interaction.response.send_message(
                f"The IP of the minecraft server is: {SERVER_IP}"
        )

    # Check status
    @discord.app_commands.command(
        name="status",
        description="Pings the minecraft server to check the status"
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
                "Server is offline or unreachable"
            )

    # Check Minecraft version
    @discord.app_commands.command(
        name="version",
        description="Shows the version of minecraft the server is running on"
    )
    async def getVersion(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            status = await asyncio.to_thread(minecraftServer.status)
            await interaction.followup.send(
                f"The server is using Minecraft version: {status.version.name}"
            )

        except (TimeoutError, OSError):
            await interaction.followup.send(
                "Server is offline or unreachable"
            )

    # playerlist
    @discord.app_commands.command(
        name="playerlist",
        description="Shows a list of the players online"
    )
    async def getPlayerlist(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
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

            await interaction.followup.send(
                f"Players: `{status.players.online}/{status.players.max}`\n"
                "\n"
                f"{playerListOutput}"
            )

        except (TimeoutError, OSError):
            await interaction.followup.send(
                "Server is offline or unreachable"
            )

async def setup(bot):
    await bot.add_cog(Commands(bot))