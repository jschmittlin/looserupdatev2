import logging

import discord
from discord import app_commands
from discord.ext import commands

from ...data import Region
from ...core import LooserUpdateV2Bot, Embed

LOGGER = logging.getLogger("looserupdatev2.region")


class Region(commands.Cog):
    def __init__(
        self, bot: LooserUpdateV2Bot
    ) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="set-region", description="Set the default region.")
    @app_commands.describe(region="Region")
    @app_commands.choices(region=[app_commands.Choice(name=str(r), value=r.value) for r in Region])
    async def region_command(
        self, interaction: discord.Interaction, region: app_commands.Choice[str],
    ) -> None:
        await interaction.response.defer()

        self.bot.settings.default_region = region.value

        embed = Embed.region_edit(region=region.value)

        await interaction.followup.send(embed=embed)
