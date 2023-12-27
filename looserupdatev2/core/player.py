from typing import Mapping, Any, Optional, List, Tuple
import logging

from .common import CoreData, LolObject
from .summoner import Summoner
from .match import MatchHistory, Match
from .staticdata import ProfileIcon
from ..data import Region, Platform, Tier, Division, Rank, Queue
from ..dto import player as dto

LOGGER = logging.getLogger("looserupdatev2.player")


##############
# Data Types #
##############


class PlayerData(CoreData):
    _dto_type = dto.PlayerDto
    _renamed = {}

class PlayerListData(CoreData):
    _file = "players.json"
    _dto_type = dto.PlayerListDto
    _renamed = {}

    def __call__(self, **kwargs):
        if "data" in kwargs:
            self.data = [Player(**player) for player in kwargs.pop("data")]
        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


class Player(LolObject):
    _data_types = {PlayerData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self) -> str:
        try:
            region = self.region
        except AttributeError:
            region = "?"
        try:
            name = self._data[PlayerData].name
        except AttributeError:
            name = "?"
        try:
            rank = self.rank
        except AttributeError:
            rank = "?"
        return "Player(region={region}, name={name}, rank={rank})".format(
            region=region, name=name, rank=rank,
        )

    def to_dict(self) -> Mapping[str, Any]:
        return {
            "region": self._data[PlayerData].region,
            "id": self._data[PlayerData].id,
            "puuid": self._data[PlayerData].puuid,
            "gameName": self._data[PlayerData].gameName,
            "tagLine": self._data[PlayerData].tagLine,
            "name": self._data[PlayerData].name,
            "profileIconId": self._data[PlayerData].profileIconId,
            "tier": self._data[PlayerData].tier,
            "division": self._data[PlayerData].division,
            "leaguePoints": self._data[PlayerData].leaguePoints,
            "wins": self._data[PlayerData].wins,
            "losses": self._data[PlayerData].losses,
            "matchId": self._data[PlayerData].matchId,
            "description": self._data[PlayerData].description,
        }

    def update_rank(self) -> bool:
        summoner = Summoner(region=self.region, puuid=self.puuid)

        try:
            match_id = MatchHistory(region=summoner.region, puuid=summoner.puuid, queue=Queue.ranked_solo_five, count=1).ids[0]
        except IndexError:
            LOGGER.debug(f"'{self.name}' - match not found")
            return False

        if self._data[PlayerData].matchId == match_id:
            LOGGER.debug(f"'{self.name}' - no new ranked solo")
            return False

        old_rank, old_lp, old_description = self.rank, self.league_points, self.description

        try:
            solo = summoner.league_entries.solo
        except ValueError:
            solo = None

        if solo is None:
            new_tier, new_division, new_rank = Tier.unranked, Division.one, Rank(tier=Tier.unranked, division=Division.one)
            new_lp, new_wins, new_losses = 0, 0, 0

            number = int(old_description.split(" ")[1].split("/")[0]) + 1
            new_description = f"PLACEMENTS {number}/10"
        else:
            new_tier, new_division, new_rank = solo.tier, solo.division, Rank(tier=solo.tier, division=solo.division)
            new_lp, new_wins, new_losses = solo.league_points, solo.wins, solo.losses

            if old_rank == new_rank:
                lp_difference = abs(new_lp - old_lp)
                lp_sign = "+" if new_lp >= old_lp else "-"
                new_description = f"{lp_sign}{lp_difference} LP"
            elif old_rank > new_rank:
                new_description = f"DEMOTE TO {new_rank}"
            elif old_rank < new_rank:
                new_description = f"PROMOTE TO {new_rank}"

        account = summoner.account

        # Update player data
        self.game_name, self.tag_line = account.game_name, account.tag_line
        self.name, self.profile_icon = summoner.name, summoner.profile_icon.id
        self.tier, self.division = new_tier.value, new_division.value
        self.league_points, self.wins, self.losses = self.league_points, new_wins, new_losses
        self.match, self.description = match_id, new_description
        return True

    @property
    def continent(self) -> str:
        return self.region.continent

    @property
    def region(self) -> Region:
        return Region(self._data[PlayerData].region)

    @property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def id(self) -> int:
        return self._data[PlayerData].id

    @property
    def puuid(self) -> str:
        return self._data[PlayerData].puuid

    @property
    def game_name(self) -> str:
        return self._data[PlayerData].gameName

    @property
    def tag_line(self) -> str:
        return self._data[PlayerData].tagLine

    @property
    def name(self) -> str:
        return self._data[PlayerData].name

    @property
    def profile_icon(self) -> ProfileIcon:
        return ProfileIcon(id=self._data[PlayerData].profileIconId)

    @property
    def league_points(self) -> int:
        return self._data[PlayerData].leaguePoints

    @property
    def wins(self) -> int:
        return self._data[PlayerData].wins

    @property
    def losses(self) -> int:
        return self._data[PlayerData].losses

    @property
    def description(self) -> str:
        return self._data[PlayerData].description

    @property
    def tier(self) -> Tier:
        try:
            return Tier(self._data[PlayerData].tier)
        except ValueError:
            return Tier.unranked

    @property
    def division(self) -> Division:
        try:
            return Division(self._data[PlayerData].division)
        except ValueError:
            return Division.one

    @property
    def rank(self) -> Rank:
        return Rank(tier=self.tier, division=self.division)

    @property
    def match(self) -> Match:
        return Match(region=self.region, id=self._data[PlayerData].matchId)

    @property
    def summoner(self) -> Summoner:
        return Summoner(region=self.region, puuid=self.puuid)

    # Setter methods

    @game_name.setter
    def game_name(self, value: str) -> None:
        self._data[PlayerData].gameName = value

    @tag_line.setter
    def tag_line(self, value: str) -> None:
        self._data[PlayerData].tagLine = value

    @name.setter
    def name(self, value: str) -> None:
        self._data[PlayerData].name = value

    @profile_icon.setter
    def profile_icon(self, value: int) -> None:
        self._data[PlayerData].profileIconId = value

    @league_points.setter
    def league_points(self, value: int) -> None:
        self._data[PlayerData].leaguePoints = value

    @wins.setter
    def wins(self, value: int) -> None:
        self._data[PlayerData].wins = value

    @losses.setter
    def losses(self, value: int) -> None:
        self._data[PlayerData].losses = value

    @description.setter
    def description(self, value: str) -> None:
        self._data[PlayerData].description = value

    @tier.setter
    def tier(self, value: str) -> None:
        self._data[PlayerData].tier = value

    @division.setter
    def division(self, value: str) -> None:
        self._data[PlayerData].division = value

    @match.setter
    def match(self, value: int) -> None:
        self._data[PlayerData].matchId = value


class PlayerList(LolObject):
    _data_types = {PlayerListData}
    _max_size = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getitem__(self, item) -> Player:
        return self._data[PlayerListData].data[item]

    @property
    def data(self) -> List[Player]:
        return self._data[PlayerListData].data

    def to_json(self, data: Optional[Mapping[str, Any]] = None) -> None:
        if data is None:
            data = self.to_dict()
        super().to_json(data=data)

    def to_dict(self) -> Mapping[str, Any]:
        return {
            "type": "player",
            "data": [player.to_dict() for player in self.data],
        }

    def get(self, game_name: str, tag_line: str) -> Player:
        for player in self.data:
            if player.game_name == game_name and player.tag_line == tag_line:
                return player
        raise ValueError(f"'{game_name} #{tag_line}' - data not found")

    def add(self, summoner: Summoner) -> Player:
        if len(self.data) >= self._max_size:
            raise ValueError(f"max size reached ({self._max_size})")

        account = summoner.account
        game_name = account.game_name
        tag_line = account.tag_line
        pair = (game_name, tag_line)

        if pair in self.get_player_names():
            raise ValueError(f"'{game_name} #{tag_line}' - already managed")

        try:
            match_id = MatchHistory(region=summoner.region, puuid=summoner.puuid, queue=Queue.ranked_solo_five, count=1).ids[0]
        except IndexError:
            match_id = None

        try:
            solo = summoner.league_entries.solo
        except ValueError:
            solo = None

        tier = getattr(solo, "tier", None)
        division = getattr(solo, "division", None)
        league_points = getattr(solo, "league_points", None)
        wins = getattr(solo, "wins", None)
        losses = getattr(solo, "losses", None)

        player = Player(
            region=summoner.region.value,
            gameName=game_name,
            tagLine=tag_line,
            id=summoner.id,
            puuid=summoner.puuid,
            name=summoner.name,
            profileIconId=summoner.profile_icon.id,
            tier=tier.value if tier else None,
            division=division.value if division else None,
            leaguePoints=league_points,
            wins=wins,
            losses=losses,
            matchId=match_id,
            description="PLACEMENTS 0/10",
        )
        self.data.append(player)
        self.to_json()

        return player

    def remove(self, game_name: str, tag_line: str) -> Player:
        player = self.get(game_name, tag_line)
        self.data.remove(player)
        self.to_json()
        return player

    def get_player_names(self) -> List[Tuple[str, str]]:
        return [(player.game_name, player.tag_line) for player in self.data]
