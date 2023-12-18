from typing import Optional
import logging

import discord
from discord import app_commands
from discord.ext import commands

from ...data import Region
from ...core import LooserUpdateV2Bot, Embed, ProfileView
from ...looserupdatev2 import get_account, get_summoner


LOGGER = logging.getLogger("looserupdatev2.profile")


class Profile(commands.Cog):
    def __init__(
        self, bot: LooserUpdateV2Bot
    ) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="profile", description="View a selected summoner profile.")
    @app_commands.describe(name="Game Name", tag="TagLine", region="Region")
    @app_commands.choices(region=[app_commands.Choice(name=str(r), value=r.value) for r in Region])
    async def profile_command(
        self, interaction: discord.Interaction, name: str, tag: Optional[str], region: Optional[app_commands.Choice[str]],
    ) -> None:
        await interaction.response.defer()

        if region is None:
            region = self.bot.settings.default_region

        try:
            if tag is None:
                summoner = get_summoner(name=name, region=region)
                account = summoner.account
            else:
                tag = tag[1:] if tag.startswith("#") else tag
                account = get_account(game_name=name, tag_line=tag, region=region)
                summoner = account.summoner

            challenges = summoner.challenges
            masteries = summoner.champion_masteries
            league = summoner.league_entries
            history = summoner.match_history
        except Exception as error:
            embed = Embed.error_summoner(error=error)
            return await interaction.followup.send(embed=embed)

        try:
            embed = Embed.profile_overview(
                summoner=summoner,
                account=account,
                challenges=challenges,
                masteries=masteries,
                league=league,
            )
            view = ProfileView(
                summoner=summoner,
                account=account,
                challenges=challenges,
                masteries=masteries,
                league=league,
                history=history,
            )
        except Exception as error:
            embed = Embed.error_summoner(error=error)
            return await interaction.followup.send(embed=embed)

        await interaction.followup.send(embed=embed, view=view)
