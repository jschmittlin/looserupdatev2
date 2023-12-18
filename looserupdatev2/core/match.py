from typing import Union, Optional, List
import datetime
import itertools

from .common import CoreData, LolObject
from .summoner import Summoner
from .staticdata import (
    Champion,
    Item,
    Items,
    Rune,
    SummonerSpell,
    Augment,
)
from ..data import (
    Continent,
    Region,
    Platform,
    Tier,
    GameType,
    GameMode,
    MatchType,
    Queue,
    Lane,
    Role,
)
from ..dto import match as dto


##############
# Data Types #
##############


class MatchListData(CoreData):
    _api = "MatchAPI"
    _dto_type = dto.MatchListDto
    _renamed = {}

class MatchData(CoreData):
    _api = "MatchAPI"
    _dto_type = dto.MatchDto
    _renamed = {
        "gameId": "id",
        "gameMode": "mode",
        "gameType": "type",
        "queueId": "queue",
        "platformId": "platform",
    }

    def __call__(self, **kwargs):
        if "gameEndTimestamp" in kwargs:
            self.end = kwargs.pop("gameEndTimestamp") // 1000
        if "gameDuration" in kwargs:
            self.duration = str(datetime.timedelta(seconds=kwargs.pop("gameDuration"))).lstrip("0:")

        if "participants" in kwargs:
            self.participants = [
                Participant(**entry) for entry in (kwargs.pop("participants") or [])
            ]
        if "teams" in kwargs:
            self.teams = [
                Team(**entry) for entry in (kwargs.pop("teams") or [])
            ]

        super().__call__(**kwargs)
        return self

class ParticipantData(CoreData):
    _dto_type = dto.ParticipantDto
    _renamed = {
        "goldEarned": "totalGold",
        "champLevel": "championLevel",
        "summoner1Id": "summonerSpell1Id",
        "summoner2Id": "summonerSpell2Id",
        "gameEndedInEarlySurrender": "remake",
    }

    def __call__(self, **kwargs):
        perks = kwargs.pop("perks", {})
        styles = perks.pop("styles", [])
        selections = list(itertools.chain(*[style.pop("selections", []) for style in styles]))
        
        self.perks = [perk["perk"] for perk in selections]
        self.items = [str(kwargs.pop(f"item{i}", None)) for i in range(7)]
        self.augments = [kwargs.pop(f"playerAugment{i}", None) for i in range(1, 5)]
        self.creepScore = kwargs.pop("totalMinionsKilled") + kwargs.pop("neutralMinionsKilled")

        super().__call__(**kwargs)
        return self

class TeamData(CoreData):
    _dto_type = dto.TeamDto
    _renamed = {}

    def __call__(self, **kwargs):
        if "bans" in kwargs:
            self.bans = [
                Ban(**entry) for entry in (kwargs.pop("bans") or [])
            ]
        if "objectives" in kwargs:
            self.objectives = Objectives(**kwargs.pop("objectives"))
        super().__call__(**kwargs)
        return self

class BanData(CoreData):
    _dto_type = dto.BanDto
    _renamed = {}

class ObjectivesData(CoreData):
    _dto_type = dto.ObjectivesDto
    _renamed = {}

    def __call__(self, **kwargs):
        if "baron" in kwargs:
            self.baron = Objective(**kwargs.pop("baron"))
        if "dragon" in kwargs:
            self.dragon = Objective(**kwargs.pop("dragon"))
        if "inhibitor" in kwargs:
            self.inhibitor = Objective(**kwargs.pop("inhibitor"))
        if "riftHerald" in kwargs:
            self.riftHerald = Objective(**kwargs.pop("riftHerald"))
        if "tower" in kwargs:
            self.tower = Objective(**kwargs.pop("tower"))
        super().__call__(**kwargs)
        return self

class ObjectiveData(CoreData):
    _dto_type = dto.ObjectiveDto
    _renamed = {}


##############
# Core Types #
##############


class MatchHistory(LolObject):
    _data_types = {MatchListData}

    def __init__(
        self,
        *,
        region: Union[Region, str] = None,
        puuid: str,
        queue: Queue = None,
        type: MatchType = None,
        start: int = None,
        count: int = None,
    ):
        if isinstance(region, str):
            region = Region(region)
        kwargs = {
            "region": region, "puuid": puuid,
        }
        if queue is not None:
            kwargs["queue"] = queue
        if type is not None:
            kwargs["type"] = type
        if start is not None:
            kwargs["start"] = start
        if count is not None:
            kwargs["count"] = count
        super().__init__(**kwargs)

    def __getitem__(self, item: Union[str, int]) -> "Match":
        return Match(region=self.region, id=self._data[MatchListData].match_ids[item])

    def __call__(self, **kwargs) -> "MatchHistory":
        kwargs.setdefault("queue", self.queue)
        kwargs.setdefault("type", self.match_type)
        kwargs.setdefault("start", self.start)
        kwargs.setdefault("count", self.count)
        return MatchHistory(**kwargs)

    @property
    def continent(self) -> Continent:
        return self.region.continent

    @property
    def region(self) -> Region:
        return self._data[MatchListData].region

    @property
    def platform(self) -> Platform:
        return Platform.from_region(self.region)

    @property
    def queue(self) -> Queue:
        return Queue(self._data[MatchListData].queue)

    @property
    def match_type(self) -> MatchType:
        return MatchType(self._data[MatchListData].type)

    @property
    def start(self) -> Union[int, None]:
        try:
            return self._data[MatchListData].start
        except AttributeError:
            return None

    @property
    def count(self) -> Union[int, None]:
        try:
            return self._data[MatchListData].count
        except AttributeError:
            return None

    @property
    def ids(self) -> List[str]:
        return self._data[MatchListData].match_ids

class Match(LolObject):
    _data_types = {MatchData}

    def __init__(
        self,
        *,
        region: Union[Region, str] = None,
        platform: Union[Platform, str] = None,
        id: str = None,
    ):
        if isinstance(platform, str):
            platform = Platform(platform)
        if isinstance(region, str):
            region = Region(region)
        if platform is None:
            platform = region.platform
        kwargs = {
            "platform": platform, "id": id,
        }
        super().__init__(**kwargs)

    @property
    def continent(self) -> Continent:
        return self.platform.continent
    
    @property
    def region(self) -> Region:
        return self.platform.region

    @property
    def platform(self) -> Platform:
        return Platform(self._data[MatchData].platform)

    @property
    def id(self) -> str:
        return self._data[MatchData].id

    @property
    def queue(self) -> Queue:
        return Queue.from_id(self._data[MatchData].queue)

    @property
    def type (self) -> MatchType:
        return MatchType(self._data[MatchData].type)

    @property
    def game_type(self) -> GameType:
        return GameType(self._data[MatchData].type)

    @property
    def mode(self) -> GameMode:
        return GameMode(self._data[MatchData].mode)

    @property
    def duration(self) -> int:
        return self._data[MatchData].duration

    @property
    def end(self) -> int:
        return self._data[MatchData].end

    @property
    def participants(self) -> List["Participant"]:
        return self._data[MatchData].participants

    @property
    def teams(self) -> List["Team"]:
        return self._data[MatchData].teams

class Participant(LolObject):
    _data_types = {ParticipantData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def assists(self) -> int:
        return self._data[ParticipantData].assists

    @property
    def champion(self) -> Champion:
        return Champion(key=self._data[ParticipantData].championId)

    @property
    def level(self) -> int:
        return self._data[ParticipantData].championLevel

    @property
    def deaths(self) -> int:
        return self._data[ParticipantData].deaths

    @property
    def gold(self) -> int:
        return self._data[ParticipantData].totalGold

    @property
    def damage_dealt(self) -> int:
        return self._data[ParticipantData].totalDamageDealtToChampions

    @property
    def damage_taken(self) -> int:
        return self._data[ParticipantData].totalDamageTaken

    @property
    def crowd_control(self) -> int:
        return self._data[ParticipantData].timeCCingOthers

    @property
    def items(self) -> List[Item]:
        return Items(included_data=self._data[ParticipantData].items)

    @property
    def kills(self) -> int:
        return self._data[ParticipantData].kills

    @property
    def creep_score(self) -> int:
        return self._data[ParticipantData].creepScore

    @property
    def runes(self) -> List[Rune]:
        return [Rune(id=id) for id in self._data[ParticipantData].perks]

    @property
    def augments(self) -> List[int]:
        return [Augment(id=id) for id in self._data[ParticipantData].augments]

    @property
    def subteam_id(self) -> int:
        return self._data[ParticipantData].playerSubteamId

    @property
    def subteam_placement(self) -> int:
        return self._data[ParticipantData].subteamPlacement

    @property
    def puuid(self) -> str:
        return self._data[ParticipantData].puuid

    @property
    def spell_d(self) -> int:
        return SummonerSpell(key=self._data[ParticipantData].summonerSpell1Id)

    @property
    def spell_f(self) -> int:
        return SummonerSpell(key=self._data[ParticipantData].summonerSpell2Id)

    @property
    def name(self) -> str:
        return self._data[ParticipantData].summonerName

    @property
    def riot_game_name(self) -> str:
        return self._data[ParticipantData].riotIdGameName

    @property
    def riot_tag_line(self) -> str:
        return self._data[ParticipantData].riotIdTagline

    @property
    def team_id(self) -> int:
        return self._data[ParticipantData].teamId

    @property
    def position(self) -> Lane:
        return Lane.from_match_naming_scheme(self._data[ParticipantData].teamPosition)

    @property
    def role(self) -> Role:
        return Role.from_match_naming_scheme(self._data[ParticipantData].role)

    @property
    def win(self) -> bool:
        return self._data[ParticipantData].win

    @property
    def remake(self) -> bool:
        return self._data[ParticipantData].remake

class Team(LolObject):
    _data_types = {TeamData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def bans(self) -> List["Ban"]:
        return self._data[TeamData].bans

    @property
    def objectives(self) -> "Objectives":
        return self._data[TeamData].objectives

    @property
    def id(self) -> int:
        return self._data[TeamData].teamId

    @property
    def win(self) -> bool:
        return self._data[TeamData].win

class Ban(LolObject):
    _data_types = {BanData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def champion(self) -> Champion:
        return Champion(key=self._data[BanData].championId)

class Objective(LolObject):
    _data_types = {ObjectiveData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def kills(self) -> int:
        return self._data[ObjectiveData].kills

class Objectives(LolObject):
    _data_types = {ObjectivesData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def baron(self) -> Objective:
        return self._data[ObjectivesData].baron

    @property
    def dragon(self) -> Objective:
        return self._data[ObjectivesData].dragon

    @property
    def inhibitor(self) -> Objective:
        return self._data[ObjectivesData].inhibitor

    @property
    def rift_herald(self) -> Objective:
        return self._data[ObjectivesData].riftHerald

    @property
    def tower(self) -> Objective:
        return self._data[ObjectivesData].tower
