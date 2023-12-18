from typing import List
from datetime import datetime
import logging
import discord
from discord import ui

from .embed import Embed
from .summoner import Summoner
from .player import Player
from .match import Match, MatchHistory
from .account import Account
from .challenges import PlayerInfo
from .championmastery import ChampionMasteries
from .league import LeagueEntries

from ..data import Queue
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
        self,
        summoner: Summoner = None,
        account: Account = None,
        challenges: PlayerInfo = None,
        masteries: ChampionMasteries = None,
        league: LeagueEntries = None,
        history: MatchHistory = None,
    ) -> None:
        super().__init__()
        self.__summoner = summoner
        self.__account = account
        self.__challenges = challenges
        self.__masteries = masteries
        self.__league = league
        self.__history = history
        self.__matchs = [match for match in self.__history]

        self.overview.disabled = True
        self.challenges.disabled = True
        self.history.disabled = False
        for option in self.match_select.options: option.default = False

        options = self.ui_selectOption_match(
            puuid=self.__summoner.puuid,
            matchs=self.__matchs,
        )
        if not options:
            self.match_select.disabled = True
        else:
            self.match_select.options = options

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

        embed = Embed.profile_overview(
            summoner=self.__summoner,
            account=self.__account,
            challenges=self.__challenges,
            masteries=self.__masteries,
            league=self.__league,
        )

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
            embed = Embed.profile_match_history(
                puuid=self.__summoner.puuid,
                matchs=self.__matchs,
            )
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
            embed = Embed.profile_match(
                puuid=self.__summoner.puuid,
                match=self.__matchs[int(select.values[0])],
            )
        except Exception as error:
            embed = Embed.profile_match_error()

        await interaction.response.edit_message(view=self, embed=embed)

    def ui_selectOption_match(self, puuid: str, matchs: List[Match]) -> List[discord.SelectOption]:
        if matchs is None:
            return []

        options = []
        index = 0
        for match in matchs:
            player = next((p for p in match.participants if p.puuid == puuid), match.participants[0])
            position = f"{player.position} \u200b • \u200b " if len(str(player.position)) > 0 else ""

            if match.queue == Queue.cherry:
                if player.subteam_placement == 1:
                    win_text = f"{player.subteam_placement}ST"
                elif player.subteam_placement == 2:
                    win_text = f"{player.subteam_placement}ND"
                elif player.subteam_placement == 3:
                    win_text = f"{player.subteam_placement}RD"
                elif player.subteam_placement == 4:
                    win_text = f"{player.subteam_placement}TH"
            else:
                win_text = "REMAKE" if player.remake else ("VICTORY" if player.win else "DEFEAT")

            labed = (
                f"{win_text}"
                f" \u200b | \u200b "
                f"{player.kills} / {player.deaths} / {player.assists}"
            )
            description = (
                f"{position}"
                f"{match.queue.description}"
                " \u200b • \u200b "
                f"{match.duration}"
                " \u200b • \u200b "
                f"{datetime.fromtimestamp(match.end).strftime('%d/%m/%Y')}"
            )
            emoji = player.champion.get_emoji

            options.append(discord.SelectOption(
                label=labed,
                description=description,
                emoji=emoji,
                value=index,
             ))
            index += 1

        return options


class UpdatePlayerView(View):
    def __init__(
        self,
        player: Player = None,
        match: Match = None,
    ) -> None:
        super().__init__()
        self.__player = player
        self.__match = match

    @discord.ui.button(
        label='MATCH DETAILS',
        style=discord.ButtonStyle.grey,
        custom_id='details',
    )
    async def details(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        try:
            embed = Embed.profile_match(
                puuid=self.__player.puuid,
                match=self.__match,
            )
        except Exception as error:
            embed = Embed.profile_match_error()

        view = UpdatePlayerBackView(
            player=self.__player,
            match=self.__match,
        )

        await interaction.response.edit_message(view=view, embed=embed)

class UpdatePlayerBackView(View):
    def __init__(
        self,
        player: Player = None,
        match: Match = None,
    ) -> None:
        super().__init__()
        self.__player = player
        self.__match = match

    @discord.ui.button(
        label='RETURN',
        style=discord.ButtonStyle.grey,
        custom_id='return',
    )
    async def back(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        embed = Embed.player_update(
            player=self.__player,
            match=self.__match,
        )

        view = UpdatePlayerView(
            player=self.__player,
            match=self.__match,
        )

        await interaction.response.edit_message(view=view, embed=embed)
