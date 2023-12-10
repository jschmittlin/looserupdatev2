from typing import List
import logging

import discord
from discord import app_commands
from discord.ext import commands

from ...data import Region
from ...core import LooserUpdateV2Bot, Embed
from ...core import PlayerList
from ...looserupdatev2 import (
    get_summoner,
    get_player_list,
    remove_player,
    add_player,
)

LOGGER = logging.getLogger("looserupdatev2.player")


class Player(commands.Cog):
    def __init__(
        self, bot: LooserUpdateV2Bot,
    ) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="add-player", description="Add player to the update list.")
    @app_commands.describe(name="Player Name", region="Region")
    @app_commands.choices(region=[app_commands.Choice(name=str(r), value=r.value) for r in Region])
    async def add_player_command(
        self, interaction: discord.Interaction, name: str, region: app_commands.Choice[str],
    ) -> None:
        await interaction.response.defer()

        try:
            summoner = get_summoner(name=name, region=self.bot.settings.default_region)
        except Exception as error:
            embed = Embed.error_summoner(error=error)
            return await interaction.followup.send(embed=embed)

        try:
            player = add_player(summoner=summoner)
        except ValueError as error:
            embed = Embed.player_error(error=error)
            return await interaction.followup.send(embed=embed)

        embed = Embed.player_add(player=player)
        await interaction.followup.send(embed=embed)

    async def remove_player_autocomplete(
        self, interaction: discord.Interaction, current: str,
    ) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=f"{player.name} #{player.region.value}", value=player.name)
            for player in get_player_list()
            if current.lower() in player.name.lower()
        ]

    @app_commands.command(name="remove-player", description="Remove player from the update list.")
    @app_commands.describe(name="Player Name")
    @app_commands.autocomplete(name=remove_player_autocomplete)
    async def remove_player_command(
        self, interaction: discord.Interaction, name: str,
    ) -> None:
        await interaction.response.defer()

        try:
            player = remove_player(name=name)
        except ValueError as error:
            embed = Embed.player_error(error=error)
            return await interaction.followup.send(embed=embed)

        embed = Embed.player_remove(player=player)
        await interaction.followup.send(embed=embed)


    @app_commands.command(name="player-list", description="View update list of players.")
    async def player_list_command(
        self, interaction: discord.Interaction,
    ) -> None:
        await interaction.response.defer()

        embed = Embed.player_list(players=get_player_list())
        await interaction.followup.send(embed=embed)