from typing import Mapping, Optional, List, Any
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
            new_tier, new_division, new_rank, new_lp = Tier.unranked, Division.one, Rank(tier=Tier.unranked, division=Division.one), 0

            number = int(old_description.split(" ")[1].split("/")[0]) + 1
            new_description = f"PLACEMENTS {number}/10"
        else:
            new_tier, new_division, new_rank, new_lp = solo.tier, solo.division, Rank(tier=solo.tier, division=solo.division), solo.league_points

            if old_rank == new_rank:
                lp_difference = abs(new_lp - old_lp)
                new_description = f"{lp_difference} LP"
            elif old_rank > new_rank:
                new_description = f"DEMOTE TO {new_rank}"
            elif old_rank < new_rank:
                new_description = f"PROMOTE TO {new_rank}"

        # Update player data
        self.name, self.profile_icon = summoner.name, summoner.profile_icon.id
        self.tier, self.division, self.league_points, self.match, self.description = new_tier.value, new_division.value, new_lp, match_id, new_description
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

    @game_name.setter
    def game_name(self, value: str) -> None:
        self._data[PlayerData].gameName = value

    @property
    def tag_line(self) -> str:
        return self._data[PlayerData].tagLine

    @tag_line.setter
    def tag_line(self, value: str) -> None:
        self._data[PlayerData].tagLine = value

    @property
    def name(self) -> str:
        return self._data[PlayerData].name

    @name.setter
    def name(self, value: str) -> None:
        self._data[PlayerData].name = value

    @property
    def profile_icon(self) -> ProfileIcon:
        return ProfileIcon(id=self._data[PlayerData].profileIconId)

    @profile_icon.setter
    def profile_icon(self, value: int) -> None:
        self._data[PlayerData].profileIconId = value

    @property
    def league_points(self) -> int:
        return self._data[PlayerData].leaguePoints

    @league_points.setter
    def league_points(self, value: int) -> None:
        self._data[PlayerData].leaguePoints = value

    @property
    def wins(self) -> int:
        return self._data[PlayerData].wins

    @wins.setter
    def wins(self, value: int) -> None:
        self._data[PlayerData].wins = value

    @property
    def losses(self) -> int:
        return self._data[PlayerData].losses

    @losses.setter
    def losses(self, value: int) -> None:
        self._data[PlayerData].losses = value

    @property
    def description(self) -> str:
        return self._data[PlayerData].description

    @description.setter
    def description(self, value: str) -> None:
        self._data[PlayerData].description = value

    @property
    def tier(self) -> Tier:
        try:
            return Tier(self._data[PlayerData].tier)
        except ValueError:
            return Tier.unranked

    @tier.setter
    def tier(self, value: str) -> None:
        self._data[PlayerData].tier = value

    @property
    def division(self) -> Division:
        try:
            return Division(self._data[PlayerData].division)
        except ValueError:
            return Division.one

    @division.setter
    def division(self, value: str) -> None:
        self._data[PlayerData].division = value

    @property
    def rank(self) -> Rank:
        return Rank(tier=self.tier, division=self.division)

    @property
    def match(self) -> Match:
        return Match(region=self.region, id=self._data[PlayerData].matchId)

    @match.setter
    def match(self, value: int) -> None:
        self._data[PlayerData].matchId = value

    @property
    def summoner(self) -> Summoner:
        return Summoner(region=self.region, puuid=self.puuid)


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

    def get(self, name: str) -> Player:
        for player in self.data:
            if player.name == name:
                return player
        raise ValueError(f"'{name}' - data not found")

    def add(self, summoner: Summoner) -> Player:
        name = summoner.name
        if name in self.get_player_names():
            raise ValueError(f"'{name}' - already managed")

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

    def remove(self, name: str) -> Player:
        player = self.get(name)
        self.data.remove(player)
        self.to_json()
        return player

    def get_player_names(self) -> List[str]:
        return [player.name for player in self.data]
