import logging

import discord
from discord import app_commands
from discord.ext import commands

from ...core import LooserUpdateV2Bot, Embed

LOGGER = logging.getLogger("looserupdatev2.help")


class Help(commands.Cog):
    def __init__(
        self, bot: LooserUpdateV2Bot,
    ) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="help", description="Show all commands and their description.")
    async def help_command(
        self, interaction: discord.Interaction,
    ) -> None:
        await interaction.response.defer()

        guild = self.bot.settings.discord_guild_object
        commands = self.bot.tree.get_commands(guild=guild)
        
        embed = Embed.help(commands=commands)

        await interaction.followup.send(embed=embed)
