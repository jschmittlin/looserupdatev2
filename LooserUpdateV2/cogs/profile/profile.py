from typing import Optional
import logging

import discord
from discord import app_commands
from discord.ext import commands

from ...data import Region
from ...core import LooserUpdateV2Bot, Embed, ProfileView
from ...looserupdatev2 import get_summoner


LOGGER = logging.getLogger("looserupdatev2.profile")


class Profile(commands.Cog):
    def __init__(
        self, bot: LooserUpdateV2Bot
    ) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="profile", description="View a selected summoner profile.")
    @app_commands.describe(name="Player Name", region="Region")
    @app_commands.choices(region=[app_commands.Choice(name=str(r), value=r.value) for r in Region])
    async def profile_command(
        self, interaction: discord.Interaction, name: str, region: Optional[app_commands.Choice[str]] = None,
    ) -> None:
        await interaction.response.defer()

        if region is None:
            region = self.bot.settings.default_region

        try:
            summoner = get_summoner(name=name, region=region)
        except Exception as error:
            embed = Embed.error_summoner(error=error)
            return await interaction.followup.send(embed=embed)

        try:
            embed = Embed.profile_overview(summoner=summoner)
        except Exception as error:
            embed = Embed.error(type="embed", error=error)
            return await interaction.followup.send(embed=embed)

        try:
            view = ProfileView(summoner=summoner)
        except Exception as error:
            embed = Embed.error(type="view", error=error)
            return await interaction.followup.send(embed=embed)

        await interaction.followup.send(embed=embed, view=view)
