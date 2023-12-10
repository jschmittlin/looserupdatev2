from .common import EmojiObject
from ..common import (
    CoreData,
    LolObject,
    ddragon,
)
from ...dto.staticdata import summonerspell as dto


##############
# Data Types #
##############


class SummonerSpellData(CoreData):
    _dto_type = dto.SummonerSpellDto
    _renamed = {}

class SummonerSpellEmoji(EmojiObject):
    _file = "summonerspells.json"
    _data_type = "summonerspell"
    _data_default = {
        "type": _data_type,
        "data": {
            "__undefined__": "<:__undef__:1179801750245490748>",
        }
    }

    def __init__(self):
        super().__init__()


##############
# Core Types #
##############


class SummonerSpell(LolObject):
    _data_types = {SummonerSpellData, SummonerSpellEmoji}
    _version = None
    _data_dragon = None

    def __init__(
        self,
        *,
        id: str = None,
        key: str = None,
    ):
        self._data = {_type: None for _type in self._data_types}
        results = {_type: {} for _type in self._data_types}

        param = next((x for x in [("id", id), ("key", key)] if x[1] is not None), None)
        if param is None:
            return

        key, value = param
        data = ddragon["cache"]["summoner.json"]["data"]

        for spell in data.values():
            if spell[key] == str(value):
                results[SummonerSpellData] = {
                    "id": spell["id"], "name": spell["name"], "key": spell["key"], "image": spell["image"]["full"],
                }
                break

        for _type, insert_this in results.items():
            if self._data[_type] is not None:
                self._data[_type] = self._data[_type](**insert_this)
            else:
                self._data[_type] = _type(**insert_this)

    def __str__(self):
        id = "?"
        name = "?"
        key = "?"
        if hasattr(self._data[SummonerSpellData], "id"):
            id = self._data[SummonerSpellData].id
        if hasattr(self._data[SummonerSpellData], "name"):
            name = self._data[SummonerSpellData].name
        if hasattr(self._data[SummonerSpellData], "key"):
            key = self._data[SummonerSpellData].key
        return "SummonerSpell(id={id}, name={name}, key={key})".format(
            id=id, name=name, key=key,
        )

    @property
    def id(self) -> str:
        return self._data[SummonerSpellData].id
    
    @property
    def key(self) -> str:
        return self._data[SummonerSpellData].key

    @property
    def name(self) -> str:
        return self._data[SummonerSpellData].name

    @property
    def image(self) -> str:
        return self._data[SummonerSpellData].image

    @property
    def url(self) -> str:
        return "https://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{image}".format(
            version=ddragon["version"], image=self._data[SummonerSpellData].image,
        )

    @property
    def emoji(self) -> "EmojiObject":
        return self._data[SummonerSpellEmoji]

    @property
    def get_emoji(self) -> str:
        return self._data[SummonerSpellEmoji].get_emoji(self._data[SummonerSpellData].id)
