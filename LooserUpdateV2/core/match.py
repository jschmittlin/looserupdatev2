from typing import Union, Optional, List
import datetime
import itertools

from .common import CoreData, LolObject
from .summoner import Summoner
from .staticdata import Champion
from .staticdata import Item, Items
from .staticdata import Rune
from .staticdata import SummonerSpell
from ..data import (
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
    _renamed = {}

    def __call__(self, **kwargs):
        if "info" in kwargs:
            self.info = Info(**kwargs.pop("info"))
        super().__call__(**kwargs)
        return self

class InfoData(CoreData):
    _api = None
    _dto_type = dto.InfoDto
    _renamed = {
        "gameMode": "mode",
        "queueId": "queue",
    }

    def __call__(self, **kwargs):
        if "participants" in kwargs:
            self.participants = [
                Participant(**entry) for entry in (kwargs.pop("participants") or [])
            ]
        if "teams" in kwargs:
            self.teams = [
                Team(**entry) for entry in (kwargs.pop("teams") or [])
            ]
        if "gameEndTimestamp" in kwargs:
            self.endTimestamp = kwargs.pop("gameEndTimestamp") // 1000
        if "gameDuration" in kwargs:
            self.duration = str(datetime.timedelta(seconds=kwargs.pop("gameDuration"))).lstrip("0:")
        super().__call__(**kwargs)
        return self

class ParticipantData(CoreData):
    _api = None
    _dto_type = dto.ParticipantDto
    _renamed = {
        "goldEarned": "totalGold",
        "champLevel": "championLevel",
        "summoner1Id": "summonerSpell1Id",
        "summoner2Id": "summonerSpell2Id",
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
    _api = None
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
    _api = None
    _dto_type = dto.BanDto
    _renamed = {}

class ObjectivesData(CoreData):
    _api = None
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
    _api = None
    _dto_type = dto.ObjectiveDto
    _renamed = {}


##############
# Core Types #
##############


class Match(LolObject):
    _data_types = {MatchData}

    def __init__(
        self,
        *,
        region: Union[Region, str],
        id: int,
    ):
        kwargs = {
            "region": region,
            "match.id": id,
        }
        self.matchId = id
        super().__init__(**kwargs)

    def __str__(self) -> str:
        try:
            region = self._data[MatchData].region
        except AttributeError:
            region = "?"
        try:
            id = self.matchId
        except AttributeError:
            id = "?"
        return "Match(region={region}, id={id})".format(
            region=region, id=id,
        )

    @property
    def region(self) -> Region:
        return self._data[MatchData].region

    @property
    def id(self) -> int:
        return self.matchId

    @property
    def info(self) -> "Info":
        return self._data[MatchData].info

class MatchHistory(LolObject):
    _data_types = {MatchListData}

    def __init__(
        self,
        *,
        region: Union[Region, str],
        puuid: str,
        queue: Queue = None,
        type: MatchType = None,
        start: int = 0,
        count: int = 20,
    ):
        kwargs = {
            "region": region,
            "summoner.puuid": puuid,
            "start": start,
            "count": count,
            "queue": queue,
            "type": type,
        }
        super().__init__(**kwargs)

    def __getitem__(self, item: Union[str, int]) -> Match:
        return Match(region=self.region, id=self._data[MatchListData].match_ids[item])

    def __str__(self) -> str:
        history = "\n\t".join(str(match) for match in self)
        return f"MatchHistory[\n\t{history}\n]"

    @property
    def ids(self) -> List[int]:
        return self._data[MatchListData].match_ids

    @property
    def region(self) -> Region:
        return self._data[MatchListData].region

    @property
    def start(self) -> Optional[int]:
        try:
            return self._data[MatchListData].start
        except AttributeError:
            return None

    @property
    def count(self) -> Optional[int]:
        try:
            return self._data[MatchListData].count
        except AttributeError:
            return None

    @property
    def queue(self) -> Queue:
        try:
            return Queue(self._data[MatchListData].queue)
        except ValueError:
            return None

    @property
    def match_type(self) -> MatchType:
        try:
            return MatchType(self._data[MatchListData].type)
        except ValueError:
            return None

class Info(LolObject):
    _data_types = {InfoData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self) -> str:
        queue = self.queue if self.queue else "?"
        try:
            mode = self._data[InfoData].mode
        except AttributeError:
            mode = "?"
        try:
            duration = self._data[InfoData].duration
        except AttributeError:
            duration = "?"
        try:
            endTimestamp = self._data[InfoData].endTimestamp
        except AttributeError:
            endTimestamp = "?"
        return "Info(mode={mode}, queue={queue}, duration={duration}, endTimestamp={endTimestamp})".format(
            mode=mode, queue=queue, duration=duration, endTimestamp=endTimestamp,
        )

    @property
    def duration(self) -> int:
        return self._data[InfoData].duration

    @property
    def end_timestamp(self) -> int:
        return self._data[InfoData].endTimestamp

    @property
    def game_mode(self) -> GameMode:
        return GameMode(self._data[InfoData].mode)

    @property
    def queue(self) -> Queue:
        return Queue.from_id(self._data[InfoData].queue)

    @property
    def participants(self) -> List["Participant"]:
        return self._data[InfoData].participants

    @property
    def teams(self) -> List["Team"]:
        return self._data[InfoData].teams

class Participant(LolObject):
    _data_types = {ParticipantData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self) -> str:
        position = self.position if self.position else "?"
        role = self.role if self.role else "?"
        try:
            name = self._data[ParticipantData].summonerName
        except AttributeError:
            name = "?"
        try:
            teamId = self._data[ParticipantData].teamId
        except AttributeError:
            teamId = "?"
        return "Participant(name={name}, teamId={teamId}, position={position}, role={role})".format(
            name=name, teamId=teamId, position=position, role=role,
        )

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
        return [Rune(id=rune_id) for rune_id in self._data[ParticipantData].perks]

    @property
    def augments(self) -> List[int]:
        return [augment for augment in self._data[ParticipantData].augments]

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

class Team(LolObject):
    _data_types = {TeamData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self) -> str:
        try:
            id = self._data[TeamData].teamId
        except AttributeError:
            id = "?"
        try:
            win = self._data[TeamData].win
        except AttributeError:
            win = "?"
        return "Team(id={id}, win={win})".format(
            id=id, win=win,
        )

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

    def __str__(self) -> str:
        champion = self.champion if self.champion else "?"
        return "Ban(champion={champion})".format(
            champion=champion,
        )

    @property
    def champion(self) -> Champion:
        return Champion(key=self._data[BanData].championId)

class Objective(LolObject):
    _data_types = {ObjectiveData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self) -> str:
        try:
            kills = self._data[ObjectiveData].kills
        except AttributeError:
            kills = "?"
        return "(kills={kills})".format(
            kills=kills,
        )

    @property
    def kills(self) -> int:
        return self._data[ObjectiveData].kills

class Objectives(LolObject):
    _data_types = {ObjectivesData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self) -> str:
        try:
            baron = self._data[ObjectivesData].baron
        except AttributeError:
            baron = "?"
        try:
            dragon = self._data[ObjectivesData].dragon
        except AttributeError:
            dragon = "?"
        try:
            inhibitor = self._data[ObjectivesData].inhibitor
        except AttributeError:
            inhibitor = "?"
        try:
            riftHerald = self._data[ObjectivesData].riftHerald
        except AttributeError:
            riftHerald = "?"
        try:
            tower = self._data[ObjectivesData].tower
        except AttributeError:
            tower = "?"
        return "Objectives(baron={baron}, dragon={dragon}, inhibitor={inhibitor}, riftHerald={riftHerald}, tower={tower})".format(
            baron=baron, dragon=dragon, inhibitor=inhibitor, riftHerald=riftHerald, tower=tower,
        )

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
