from typing import Union, List

from .common import CoreData, LolObject
from .summoner import Summoner
from .staticdata.challenges import ChallengeTitle
from ..data import Region, Platform
from ..dto import challenges as dto


##############
# Data Types #
##############


class PlayerInfoData(CoreData):
    _api = "ChallengesAPI"
    _dto_type = dto.PlayerInfoDto
    _renamed = {}

    def __call__(self, **kwargs):
        if "totalPoints" in kwargs:
            self.totalPoints = ChallengePoints(**kwargs.pop("totalPoints"))
        if "categoryPoints" in kwargs:
            self.categoryPoints = CategoryPoints(**kwargs.pop("categoryPoints"))
        if "preferences" in kwargs:
            self.preferences = PlayerClientPreferences(**kwargs.pop("preferences"))
        super().__call__(**kwargs)
        return self

class PlayerClientPreferencesData(CoreData):
    _api = None
    _dto_type = dto.PlayerClientPreferencesDto
    _renamed = {}

class ChallengePointsData(CoreData):
    _api = None
    _dto_type = dto.ChallengePointsDto
    _renamed = {}

class CategoryPointsData(CoreData):
    _api = None
    _dto_type = dto.CategoryPointsDto
    _renamed = {
        "EXPERTISE": "expertise",
        "VETERANCY": "veterancy",
        "COLLECTION": "collection",
        "TEAMWORK": "teamwork",
        "IMAGINATION": "imagination",
    }

    def __call__(self, **kwargs):
        if "EXPERTISE" in kwargs:
            self.expertise = ChallengePoints(**kwargs.pop("EXPERTISE"))
        if "VETERANCY" in kwargs:
            self.veterancy = ChallengePoints(**kwargs.pop("VETERANCY"))
        if "COLLECTION" in kwargs:
            self.collection = ChallengePoints(**kwargs.pop("COLLECTION"))
        if "TEAMWORK" in kwargs:
            self.teamwork = ChallengePoints(**kwargs.pop("TEAMWORK"))
        if "IMAGINATION" in kwargs:
            self.imagination = ChallengePoints(**kwargs.pop("IMAGINATION"))
        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


class PlayerInfo(LolObject):
    _data_types = {PlayerInfoData}

    def __init__(self, *, summoner: Summoner):
        self.__summoner__ = summoner
        kwargs = {
            "region": summoner.region,
            "summoner.puuid": summoner.puuid,
        }
        super().__init__(**kwargs)

    @property
    def summoner(self) -> Summoner:
        return self.__summoner__

    @property
    def total_points(self) -> int:
        return self._data[PlayerInfoData].totalPoints

    @property
    def category_points(self) -> "CategoryPoints":
        return self._data[PlayerInfoData].categoryPoints

    @property
    def preferences(self) -> "PlayerClientPreferences":
        return self._data[PlayerInfoData].preferences

class PlayerClientPreferences(LolObject):
    _data_types = {PlayerClientPreferencesData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self) -> str:
        title = self.title if self.title is not None else "?"
        try:
            challengeIds = self._data[PlayerClientPreferencesData].challengeIds
        except AttributeError:
            challengeIds = "?"
        return "PlayerClientPreferences(title={title}, challengeIds={challengeIds})".format(
            title=title, challengeIds=challengeIds,
        )

    @property
    def title(self) -> str:
        return ChallengeTitle(id=self._data[PlayerClientPreferencesData].title)

    @property
    def challenge_ids(self) -> List[int]:
        return self._data[PlayerClientPreferencesData].challengeIds

class CategoryPoints(LolObject):
    _data_types = {CategoryPointsData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
   
    def __str__(self) -> str:
        try:
            expertise = self._data[CategoryPointsData].expertise
        except AttributeError:
            expertise = "?"
        try:
            veterancy = self._data[CategoryPointsData].veterancy
        except AttributeError:
            veterancy = "?"
        try:
            collection = self._data[CategoryPointsData].collection
        except AttributeError:
            collection = "?"
        try:
            teamwork = self._data[CategoryPointsData].teamwork
        except AttributeError:
            teamwork = "?"
        try:
            imagination = self._data[CategoryPointsData].imagination
        except AttributeError:
            imagination = "?"
        return "ChallengesCategory(expertise={expertise}, veterancy={veterancy}, collection={collection}, teamwork={teamwork}, imagination={imagination})".format(
            expertise=expertise, veterancy=veterancy, collection=collection, teamwork=teamwork, imagination=imagination,
        )

    @property
    def expertise(self) -> "ChallengePoints":
        return self._data[CategoryPointsData].expertise

    @property
    def veterancy(self) -> "ChallengePoints":
        return self._data[CategoryPointsData].veterancy

    @property
    def collection(self) -> "ChallengePoints":
        return self._data[CategoryPointsData].collection

    @property
    def teamwork(self) -> "ChallengePoints":
        return self._data[CategoryPointsData].teamwork

    @property
    def imagination(self) -> "ChallengePoints":
        return self._data[CategoryPointsData].imagination

class ChallengePoints(LolObject):
    _data_types = {ChallengePointsData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self) -> str:
        try:
            level = self._data[ChallengePointsData].level
        except AttributeError:
            level = "?"
        try:
            current = self._data[ChallengePointsData].current
        except AttributeError:
            current = "?"
        try:
            max = self._data[ChallengePointsData].max
        except AttributeError:
            max = "?"
        return "ChallengePoints(level={level}, current={current}, max={max})".format(
            level=level, current=current, max=max,
        )

    @property
    def level(self) -> str:
        return self._data[ChallengePointsData].level

    @property
    def current(self) -> int:
        return self._data[ChallengePointsData].current

    @property
    def maximum(self) -> int:
        return self._data[ChallengePointsData].max
