from typing import Union

from .common import CoreData, LolObject
from .summoner import Summoner
from ..data import Region, Platform, Tier, Division, Queue
from ..dto import league as dto


##############
# Data Types #
##############


class LeagueEntryData(CoreData):
    _dto_type = dto.LeagueEntryDto
    _renamed = {
        "queueType": "queue",
        "rank": "division",
    }

class LeagueEntriesData(CoreData):
    _api = "LeagueAPI"
    _dto_type = dto.LeagueEntriesDto
    _renamed = {}

    def __call__(self, **kwargs):
        if "entries" in kwargs:
            self.entries = [
                LeagueEntry(**entry) for entry in (kwargs.pop("entries") or [])
            ]
        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


class LeagueEntry(LolObject):
    _data_types = {LeagueEntryData}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def region(self) -> Region:
        return Region(self._data[LeagueEntryData].region)

    def __str__(self) -> str:
        try:
            queue = self._data[LeagueEntryData].queue
        except AttributeError:
            queue = "?"
        try:
            tier = self._data[LeagueEntryData].tier
        except AttributeError:
            tier = "?"
        try:
            division = self._data[LeagueEntryData].division
        except AttributeError:
            division = "?"
        try:
            leaguePoints = self._data[LeagueEntryData].leaguePoints
        except AttributeError:
            leaguePoints = "?"
        try:
            wins = self._data[LeagueEntryData].wins
        except AttributeError:
            wins = "?"
        try:
            losses = self._data[LeagueEntryData].losses
        except AttributeError:
            losses = "?"
        return "League(queue={queue}, tier={tier}, division={division}, leaguePoints={leaguePoints}, wins={wins}, losses={losses})".format(
            queue=queue, tier=tier, division=division, leaguePoints=leaguePoints, wins=wins, losses=losses
        )

    @property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def queue(self) -> Queue:
        return Queue(self._data[LeagueEntryData].queue)

    @property
    def tier(self) -> Tier:
        return Tier(self._data[LeagueEntryData].tier)

    @property
    def division(self) -> Division:
        return Division(self._data[LeagueEntryData].division)

    @property
    def league_points(self) -> int:
        return self._data[LeagueEntryData].leaguePoints

    @property
    def wins(self) -> int:
        return self._data[LeagueEntryData].wins

    @property
    def losses(self) -> int:
        return self._data[LeagueEntryData].losses

    @property
    def veteran(self) -> bool:
        return self._data[LeagueEntryData].veteran

    @property
    def inactive(self) -> bool:
        return self._data[LeagueEntryData].inactive

    @property
    def fresh_blood(self) -> bool:
        return self._data[LeagueEntryData].freshBlood

    @property
    def hot_streak(self) -> bool:
        return self._data[LeagueEntryData].hotStreak

class LeagueEntries(LolObject):
    _data_types = {LeagueEntriesData}

    def __init__(
        self, summoner: Summoner
    ):
        kwargs = {
            "platform": summoner.platform, "id": summoner.id,
        }
        super().__init__(**kwargs)

    def __getitem__(self, item) -> LeagueEntry:
        return self._data[LeagueEntriesData].entries[item]

    def __len__(self) -> int:
        return len(self._data[LeagueEntriesData].entries)

    def __iter__(self) -> LeagueEntry:
        return iter(self._data[LeagueEntriesData].entries)

    @property
    def region(self) -> Region:
        return Region(self._data[LeagueEntriesData].region)

    @property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def solo(self) -> LeagueEntry:
        for entry in self._data[LeagueEntriesData].entries:
            if entry.queue is Queue.ranked_solo_five:
                return entry
        raise ValueError("Queue does not exist for this summoner.")

    @property
    def flex(self) -> LeagueEntry:
        for entry in self._data[LeagueEntriesData].entries:
            if entry.queue is Queue.ranked_flex_five:
                return entry
        raise ValueError("Queue does not exist for this summoner.")

    @property
    def arena(self) -> LeagueEntry:
        for entry in self._data[LeagueEntriesData].entries:
            if entry.queue is Queue.cherry:
                return entry
        raise ValueError("Queue does not exist for this summoner.")
