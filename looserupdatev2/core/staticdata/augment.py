from .common import EmojiObject
from ..common import (
    CoreData,
    LolObject,
    ddragon,
)
from ...dto.staticdata import augment as dto


##############
# Data Types #
##############


class AugmentData(CoreData):
    _dto_type = dto.AugmentDto
    _renamed = {}

class AugmentEmoji(EmojiObject):
    _file = "augments.json"
    _data_type = "augment"
    _data_default = {
        "type": _data_type,
        "data": {
            "__undefined__": "<:0_:1183399365616873594>",
        }
    }

    def __init__(self):
        super().__init__()


##############
# Core Types #
##############


class Augment(LolObject):
    _data_types = {AugmentData, AugmentEmoji}

    def __init__(
        self, id: int = None
    ):
        self._data = {_type: None for _type in self._data_types}
        results = {_type: {} for _type in self._data_types}

        if id is None:
            return

        if len(str(id)) == 2 and str(id).startswith("0"):
            tmp = str(id)
            id = int(tmp[1])

        data = ddragon["cache"]["spellbuffs.json"]["augments"]

        results[AugmentData] = {"id": id, "name": "__undefined__"}
        for augment in data:
            if augment["id"] == id:
                id_ = augment["id"] if len(str(augment["id"])) != 1 else f"0{augment['id']}"
                results[AugmentData] = {
                    "id": id_, "name": augment["name"], "iconLarge": augment["iconLarge"],
                }

        for _type, insert_this in results.items():
            if self._data[_type] is not None:
                self._data[_type] = self._data[_type](**insert_this)
            else:
                self._data[_type] = _type(**insert_this)

    def __str__(self) -> str:
        id = "?"
        name = "?"
        if hasattr(self._data[AugmentData], "id"):
            id = self._data[AugmentData].id
        if hasattr(self._data[AugmentData], "name"):
            name = self._data[AugmentData].name
        return "Augment(id={id}, name={name})".format(
            id=id, name=name,
        )

    @property
    def id(self) -> int:
        return self._data[AugmentData].id

    @property
    def name(self) -> str:
        return self._data[AugmentData].name

    @property
    def icon(self) -> str:
        return self._data[AugmentData].iconLarge

    @property
    def url(self) -> str:
        return "https://raw.communitydragon.org/latest/game/{icon}".format(
            icon=self._data[AugmentData].iconLarge,
        )

    @property
    def emoji(self) -> "EmojiObject":
        return self._data[AugmentEmoji]

    @property
    def get_emoji(self) -> str:
        return self._data[AugmentEmoji].get_emoji(self._data[AugmentData].id)
