from .common import EmojiObject
from ..common import (
    CoreData,
    LolObject,
    ddragon,
)
from ...dto.staticdata import rune as dto


##############
# Data Types #
##############


class RuneData(CoreData):
    _dto_type = dto.RuneDto
    _renamed = {}

class RuneEmoji(EmojiObject):
    _file = "runes.json"
    _data_type = "rune"
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


class Rune(LolObject):
    _data_types = {RuneData, RuneEmoji}
    _version = None
    _data_dragon = None

    def __init__(
        self,
        *,
        id: int = None
    ):
        self._data = {_type: None for _type in self._data_types}
        results = {_type: {} for _type in self._data_types}

        if id is None:
            return

        data = ddragon["cache"]["runesReforged.json"]

        for runeReforged in data:
            for slot in runeReforged["slots"]:
                for rune in slot["runes"]:
                    if rune["id"] == id:
                        results[RuneData] = {
                            "id": rune["id"], "name": rune["name"], "key": rune["key"], "icon": rune["icon"], 
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
        if hasattr(self._data[RuneData], "id"):
            id = self._data[RuneData].id
        if hasattr(self._data[RuneData], "name"):
            name = self._data[RuneData].name
        if hasattr(self._data[RuneData], "key"):
            key = self._data[RuneData].key
        return "Rune(id={id}, name={name}, key={key})".format(
            id=id, name=name, key=key,
        )

    @property
    def id(self) -> str:
        return self._data[RuneData].id

    @property
    def key(self) -> str:
        return self._data[RuneData].key

    @property
    def name(self) -> str:
        return self._data[RuneData].name

    @property
    def icon(self) -> str:
        return self._data[RuneData].icon

    @property
    def url(self) -> str:
        return "https://ddragon.leagueoflegends.com/cdn/img/{icon}".format(
            icon=self._data[RuneData].icon,
        )

    @property
    def emoji(self) -> "EmojiObject":
        return self._data[RuneEmoji]

    @property
    def get_emoji(self) -> str:
        try:
            return self._data[RuneEmoji].get_emoji(self._data[RuneData].id)
        except AttributeError:
            return self._data[RuneEmoji].get_emoji(0)
