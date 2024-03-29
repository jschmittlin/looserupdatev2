from typing import Union

from .common import CoreData, LolObject
from .staticdata import ProfileIcon
from ..data import Region, Platform, Rank
from ..dto import summoner as dto


MATCH_HISTORY_COUNT = 5


##############
# Data Types #
##############


class SummonerData(CoreData):
    _api = "SummonerAPI"
    _dto_type = dto.SummonerDto
    _renamed = {"summonerLevel": "level"}


##############
# Core Types #
##############


class Summoner(LolObject):
    _data_types = {SummonerData}

    def __init__(
        self,
        *,
        id: str = None,
        account_id: str = None,
        puuid: str = None,
        name: str = None,
        region: Union[Region, str] = None,
    ):
        if isinstance(region, str):
            region = Region(region)
        kwargs = {"platform": region.platform}
        if id is not None:
            kwargs["id"] = id
        if account_id is not None:
            kwargs["accountId"] = account_id
        if puuid is not None:
            kwargs["puuid"] = puuid
        if name is not None:
            kwargs["name"] = name
        super().__init__(**kwargs)

    def __eq__(self, other: "Summoner") -> bool:
        if not isinstance(other, Summoner) or self.region != other.region:
            return 
        s = {}
        o = {}
        if hasattr(self._data[SummonerData], "id"):
            s["id"] = self._data[SummonerData].id
        if hasattr(other._data[SummonerData], "id"):
            o["id"] = other._data[SummonerData].id
        if hasattr(self._data[SummonerData], "accountId"):
            s["accountId"] = self._data[SummonerData].accountId
        if hasattr(other._data[SummonerData], "accountId"):
            o["accountId"] = other._data[SummonerData].accountId
        if hasattr(self._data[SummonerData], "puuid"):
            s["puuid"] = self._data[SummonerData].puuid
        if hasattr(other._data[SummonerData], "puuid"):
            o["puuid"] = other._data[SummonerData].puuid
        if any(s.get(key, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.account_id == other.account_id

    def __str__(self) -> str:
        try:
            id = self._data[SummonerData].id
        except AttributeError:
            id = "?"
        try:
            account_id = self._data[SummonerData].accountId
        except AttributeError:
            account_id = "?"
        try:
            puuid = self._data[SummonerData].puuid
        except AttributeError:
            puuid = "?"
        try:
            name = self._data[SummonerData].name
        except AttributeError:
            name = "?"
        return "Summoner(id={id}, account_id={account_id}, puuid={puuid}, name={name})".format(
            id=id, account_id=account_id, puuid=puuid, name=name,
        )

    @property
    def continent(self) -> str:
        return self.region.continent

    @property
    def region(self) -> Platform:
        return Region(self._data[SummonerData].region)

    @property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def id(self) -> str:
        return self._data[SummonerData].id

    @property
    def account_id(self) -> str:
        return self._data[SummonerData].accountId

    @property
    def puuid(self) -> str:
        return self._data[SummonerData].puuid

    @property
    def name(self) -> str:
        return self._data[SummonerData].name

    @property
    def level(self) -> int:
        return self._data[SummonerData].level

    @property
    def revision_date(self) -> int:
        return self._data[SummonerData].revisionDate

    @property
    def profile_icon(self) -> ProfileIcon:
        return ProfileIcon(id=self._data[SummonerData].profileIconId)

    # Special core methods

    @property
    def account(self) -> "Account":
        from .account import Account

        return Account(puuid=self.puuid, region=self.region)

    @property
    def challenges(self) -> "Challenges":
        from .challenges import PlayerInfo

        return PlayerInfo(summoner=self)

    @property
    def champion_masteries(self) -> "ChampionMasteries":
        from .championmastery import ChampionMasteries

        return ChampionMasteries(summoner=self)

    @property
    def league_entries(self) -> "LeagueEntries":
        from .league import LeagueEntries

        return LeagueEntries(summoner=self)

    @property
    def match_history(self) -> "MatchHistory":
        from .match import MatchHistory

        return MatchHistory(region=self.region, puuid=self.puuid, count=MATCH_HISTORY_COUNT)

    @property
    def ranks(self):
        return {
            league.queue: Rank(tier=league.tier, division=league.division)
            for league in self.league_entries
        }
