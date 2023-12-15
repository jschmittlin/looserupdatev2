from typing import Union, List

from .common import CoreData, LolObject
from .summoner import Summoner
from .staticdata.champion import Champion
from ..data import Region, Platform
from ..dto import championmastery as dto


##############
# Data Types #
##############


class ChampionMasteryData(CoreData):
    _dto_type = dto.ChampionMasteryDto
    _renamed = {
        "championLevel": "level",
        "championPoints": "points",
    }

class ChampionMasteryListData(CoreData):
    _api = "ChampionMasteryAPI"
    _dto_type = dto.ChampionMasteryListDto
    _renamed = {}

    def __call__(self, **kwargs):
        if "championMasteryList" in kwargs:
            self.championMasteryList = [
                ChampionMastery(**entry) for entry in (kwargs.pop("championMasteryList") or [])
            ]
        super().__call__(**kwargs)
        return self

class ChampionMasteryScoreData(CoreData):
    _api = "ChampionMasteryAPI"
    _dto_type = dto.ChampionMasteryScoreDto
    _renamed = {}


##############
# Core Types #
##############


class ChampionMastery(LolObject):
    _data_types = {ChampionMasteryData}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self) -> str:
        champion = self.champion if self.champion else "?" 
        try:
            level = self._data[ChampionMasteryData].level
        except AttributeError:
            level = "?"
        try:
            points = self._data[ChampionMasteryData].points
        except AttributeError:
            points = "?"
        return "ChampionMastery(champion={champion}, level={level}, points={points})".format(
            champion=champion, level=level, points=points
        )

    @property
    def champion(self) -> Champion:
        return Champion(key=self._data[ChampionMasteryData].championId)

    @property
    def level(self) -> int:
        return self._data[ChampionMasteryData].level

    @property
    def points(self) -> int:
        return self._data[ChampionMasteryData].points

    @property
    def last_played(self) -> int:
        return self._data[ChampionMasteryData].lastPlayTime

    @property
    def points_since_last_level(self) -> int:
        return self._data[ChampionMasteryData].championPointsSinceLastLevel

    @property
    def points_until_next_level(self) -> int:
        return self._data[ChampionMasteryData].championPointsUntilNextLevel

    @property
    def chest_granted(self) -> bool:
        return self._data[ChampionMasteryData].chestGranted

    @property
    def tokens_earned(self) -> int:
        return self._data[ChampionMasteryData].tokensEarned

class ChampionMasteries(LolObject):
    _data_types = {ChampionMasteryListData, ChampionMasteryScoreData}

    def __init__(self, *, summoner: Summoner):
        self.__summoner = summoner
        kwargs = {
            "region": summoner.region, "puuid": summoner.puuid
        }
        super().__init__(**kwargs)

    @property
    def region(self) -> Region:
        return Region(self._data[ChampionMasteryListData].region)

    @property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def champion_mastery_list(self) -> List[ChampionMastery]:
        return self._data[ChampionMasteryListData].championMasteryList

    @property
    def score(self) -> int:
        return self._data[ChampionMasteryScoreData].score
