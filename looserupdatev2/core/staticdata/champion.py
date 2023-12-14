from .common import EmojiObject
from ..common import (
    CoreData,
    LolObject,
    ddragon,
)
from ...dto.staticdata import champion as dto


##############
# Data Types #
##############


class ChampionData(CoreData):
    _dto_type = dto.ChampionDto
    _renamed = {}

class ChampionEmoji(EmojiObject):
    _file = "champions.json"
    _data_type = "champion"
    _data_default = {
        "type": _data_type,
        "data": {
            "__undefined__": "<:__champion__:1181968146052169789>",
        }
    }

    def __init__(self):
        super().__init__()


##############
# Core Types #
##############


class Champion(LolObject):
    _data_types = {ChampionData, ChampionEmoji}

    def __init__(
        self,
        *,
        id: str = None,
        name: str = None,
        key: str = None,
    ):
        self._data = {_type: None for _type in self._data_types}
        results = {_type: {} for _type in self._data_types}

        param = next((x for x in [("id", id), ("name", name), ("key", key)] if x[1] is not None), None)
        if param is None:
            return

        key, value = param
        data = ddragon["cache"]["champion.json"]["data"]

        results[ChampionData] = {"id": None, "name": None, "key": None}
        for champion in data.values():
            if champion[key] == str(value):
                results[ChampionData] = {key: champion[key] for key in ["id", "name", "key"]}
                found = True
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
        if hasattr(self._data[ChampionData], "id"):
            id = self._data[ChampionData].id
        if hasattr(self._data[ChampionData], "name"):
            name = self._data[ChampionData].name
        if hasattr(self._data[ChampionData], "key"):
            key = self._data[ChampionData].key
        return "Champion(id={id}, name={name}, key={key})".format(
            id=id, name=name, key=key,
        )

    @property
    def id(self) -> str:
        return self._data[ChampionData].id

    @property
    def key(self) -> str:
        return self._data[ChampionData].key

    @property
    def name(self) -> str:
        return self._data[ChampionData].name

    @property
    def url(self) -> str:
        return "https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{id}.png".format(
            version=ddragon["version"], id=self._data[ChampionData].id,
        )

    @property
    def emoji(self) -> "EmojiObject":
        return self._data[ChampionEmoji]

    @property
    def get_emoji(self) -> str:
        return self._data[ChampionEmoji].get_emoji(self._data[ChampionData].id)
