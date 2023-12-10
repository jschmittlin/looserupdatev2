from typing import List
from datetime import datetime
import logging
import discord
from discord import ui

from .embed import Embed
from .summoner import Summoner
from .player import Player
from .match import MatchHistory

from ..resources import Icon, Color
from ..resources.emoji import blank

LOGGER = logging.getLogger("looserupdatev2.view")


class View(discord.ui.View):
    def __init__(
        self,
    ) -> None:
        super().__init__(timeout=None)

class ProfileView(View):
    def __init__(
        self, summoner: Summoner,
    ) -> None:
        super().__init__()
        self.summoner = summoner
        self.match_history = summoner.match_history
        self.overview.disabled = True
        self.challenges.disabled = True
        self.history.disabled = False
        for option in self.match_select.options: option.default = False

        # load data
        options = self.ui_selectOption_match(puuid=self.summoner.puuid, history=self.match_history)
        if not options:
            self.match_select.disabled = True
        else:
            self.match_select.options = options
            Embed.profile_match_history(summoner=self.summoner)

    def ui_selectOption_match(self, puuid: str, history: MatchHistory) -> List[discord.SelectOption]:
        if history is None: return []
        options = []
        index = 0
        for match in history:
            player = next((p for p in match.info.participants if p.puuid == puuid), match.info.participants[0])
            position = f"{player.position} \u200b • \u200b " if len(str(player.position)) > 0 else ""
            labed = (
                f"{'VICTORY' if player.win else 'DEFEAT'}"
                f" \u200b | \u200b "
                f"{player.kills} / {player.deaths} / {player.assists}"
            )
            description = (
                f"{position}"
                f"{match.info.queue.description}"
                " \u200b • \u200b "
                f"{match.info.duration}"
                " \u200b • \u200b "
                f"{datetime.fromtimestamp(match.info.end_timestamp).strftime('%d/%m/%Y')}"
            )
            emoji = player.champion.get_emoji
            options.append(discord.SelectOption(label=labed, description=description, emoji=emoji, value=index))
            index += 1
        return options

    @ui.button(
        custom_id="overview",
        label="OVERVIEW",
        style=discord.ButtonStyle.grey,
    )
    async def overview(
        self, interaction: discord.Interaction, button: ui.Button,
    ) -> None:
        self.overview.disabled = True
        self.challenges.disabled = True
        self.history.disabled = False
        for option in self.match_select.options: option.default = False

        embed = Embed.profile_overview(summoner=self.summoner)
        await interaction.response.edit_message(view=self, embed=embed)

    @ui.button(
        custom_id="challenges",
        label="CHALLENGES",
        style=discord.ButtonStyle.grey,
    )
    async def challenges(
        self, interaction: discord.Interaction, button: ui.Button,
    ) -> None:
        self.overview.disabled = False
        self.challenges.disabled = True
        self.history.disabled = False
        for option in self.match_select.options: option.default = False

        embed = Embed.profile_overview(summoner=self.summoner)
        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(
        custom_id="match_history",
        label="MATCH HISTORY", 
        style=discord.ButtonStyle.grey, 
    )
    async def history(
        self, interaction: discord.Interaction, button: discord.ui.Button,
    ) -> None:
        self.overview.disabled = False
        self.challenges.disabled = True
        self.history.disabled = True
        for option in self.match_select.options: option.default = False

        try:
            embed = Embed.profile_match_history(summoner=self.summoner)
        except IndexError:
            embed = Embed.profile_match_error()

        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.select(
        custom_id="match_select",
        placeholder="MATCH DETAILS",
        options=[
            discord.SelectOption(label="Match 1", value=0),
            discord.SelectOption(label="Match 2", value=1),
            discord.SelectOption(label="Match 3", value=2),
            discord.SelectOption(label="Match 4", value=3),
            discord.SelectOption(label="Match 5", value=4),
        ],
    )
    async def match_select(
        self, interaction=discord.Interaction, select=discord.ui.Select,
    ) -> None:
        self.overview.disabled = False
        self.challenges.disabled = True
        self.history.disabled = False
        for option in self.match_select.options: option.default = False
        select.options[int(select.values[0])].default = True

        try:
            embed = Embed.profile_match(puuid=self.summoner.puuid, match=self.match_history[int(select.values[0])])
        except Exception as error:
            LOGGER.error(error)
            embed = Embed.profile_match_error()

        try:
            await interaction.response.edit_message(view=self, embed=embed)
        except discord.errors.HTTPException as error:
            LOGGER.error(error)
            embed = Embed.profile_match_error()
            await interaction.response.send_message(view=self, embed=embed)


class UpdatePlayerView(View):
    def __init__(
        self, player: Player,
    ) -> None:
        super().__init__()
        self.player = player

    @discord.ui.button(
        label='MATCH DETAILS',
        style=discord.ButtonStyle.grey,
        custom_id='details',
    )
    async def details(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        try:
            embed = Embed.profile_match(puuid=self.player.puuid, match=self.player.match)
        except Exception as error:
            LOGGER.error(error)
            embed = Embed.profile_match_error()

        view = UpdatePlayerBackView(player=self.player)
        await interaction.response.edit_message(view=view, embed=embed)

class UpdatePlayerBackView(View):
    def __init__(
        self, player: Player,
    ) -> None:
        super().__init__()
        self.player = player

    @discord.ui.button(
        label='RETURN',
        style=discord.ButtonStyle.grey,
        custom_id='return',
    )
    async def back(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        embed = Embed.player_update(player=self.player)
        view = UpdatePlayerView(player=self.player)
        await interaction.response.edit_message(view=view, embed=embed)
