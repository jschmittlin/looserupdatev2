from typing import Union

from .common import CoreData, LolObject
from ..data import Continent, Region, Platform
from ..dto import account as dto


##############
# Data Types #
##############


class AccountData(CoreData):
    _api = "AccountAPI"
    _dto_type = dto.AccountDto
    _renamed = {}


##############
# Core Types #
##############


class Account(LolObject):
    _data_types = {AccountData}

    def __init__(
        self,
        *,
        puuid: str = None,
        game_name: str = None,
        tag_line: str = None,
        region: Union[Region, str] = None,
    ):
        kwargs = {"region": region}
        if puuid is not None:
            kwargs["puuid"] = puuid
        if game_name is not None and tag_line is not None:
            kwargs["gameName"] = game_name
            kwargs["tagLine"] = tag_line
        super().__init__(**kwargs)

    def __eq__(self, other: "Account") -> bool:
        if not isinstance(other, Account) or self.continent != other.continent:
            return False
        s = {}
        o = {}
        if hasattr(self._data[AccountData], "puuid"):
            s["puuid"] = self._data[AccountData].puuid
        if hasattr(other._data[AccountData], "puuid"):
            o["puuid"] = other._data[AccountData].puuid
        if hasattr(self._data[AccountData], "game_name"):
            s["game_name"] = self._data[AccountData].game_name
        if hasattr(other._data[AccountData], "game_name"):
            o["game_name"] = other._data[AccountData].game_name
        if hasattr(self._data[AccountData], "tag_line"):
            s["tag_line"] = self._data[AccountData].tag_line
        if hasattr(other._data[AccountData], "tag_line"):
            o["tag_line"] = other._data[AccountData].tag_line
        if any(s.get(kei, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.puuid == other.puuid

    def __str__(self) -> str:
        try:
            game_name = self._data[AccountData].gameName
        except AttributeError:
            game_name = "?"
        try:
            tag_line = self._data[AccountData].tagLine
        except AttributeError:
            tag_line = "?"
        return "Account(game_name={game_name}, tag_line={tag_line})".format(
            game_name=game_name, tag_line=tag_line,
        )

    @property
    def continent(self) -> Continent:
        return self.region.continent

    @property
    def region(self) -> Region:
        return self._data[AccountData].region

    @property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def puuid(self) -> str:
        return self._data[AccountData].puuid

    @property
    def game_name(self) -> str:
        return self._data[AccountData].gameName

    @property
    def tag_line(self) -> str:
        return self._data[AccountData].tagLine

    # Special core methods

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner

        return Summoner(puuid=self.puuid, region=self.region)
