from typing import List

from .common import EmojiObject
from ..common import (
    CoreData,
    LolObject,
    ddragon,
)
from ...dto.staticdata import item as dto


##############
# Data Types #
##############


class ItemListData(CoreData):
    _dto_type = dto.ItemListDto
    _renamed = {}

class ItemData(CoreData):
    _dto_type = dto.ItemDto
    _renamed = {}

class ItemEmoji(EmojiObject):
    _file = "items.json"
    _data_type = "item"
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


class Items(LolObject):
    _data_types = {ItemListData}
    
    def __init__(
        self, included_data: List[str] = None,
    ):
        self._data = {_type: None for _type in self._data_types}
        results = {_type: {} for _type in self._data_types}

        if included_data is None:
            return

        data = ddragon["cache"]["item.json"]["data"]
        
        results[ItemListData]["included_data"] = included_data
        results[ItemListData]["data"] = {}
        results[ItemListData]["data"]["0"] = Item(id="0", name="__undefined__")
        for key, value in data.items():
            if key in included_data:
                results[ItemListData]["data"][key] = Item(id=key, name=value["name"], image=value["image"]["full"])

        for _type, insert_this in results.items():                
            if self._data[_type] is not None:
                self._data[_type] = self._data[_type](**insert_this)
            else:
                self._data[_type] = _type(**insert_this)

    def __getitem__(self, item) -> "Item":
        return self._data[ItemListData].data[item]

    def __iter__(self):
        included_data_order = self._data[ItemListData].included_data
        return iter(self._data[ItemListData].data[key] for key in included_data_order)

    @property
    def data(self) -> List["Item"]:
        return self._data[ItemListData].data

    @property
    def included_data(self) -> List[str]:
        return self._data[ItemListData].included_data
    
class Item(LolObject):
    _data_types = {ItemData, ItemEmoji}

    def __init__(
        self,
        *,
        id: str = None,
        name: str = None,
        image: str = None,
    ):
        kwargs = {}
        if id is not None:
            kwargs["id"] = id
        if name is not None:
            kwargs["name"] = name
        if image is not None:
            kwargs["image"] = image
        super().__init__(**kwargs)

    def __str__(self):
        id = "?"
        name = "?"
        if hasattr(self._data[ItemData], "id"):
            id = self._data[ItemData].id
        if hasattr(self._data[ItemData], "name"):
            name = self._data[ItemData].name
        return "Item(id={id}, name={name})".format(
            id=id, name=name,
        )

    @property
    def id(self) -> str:
        return self._data[ItemData].id

    @property
    def name(self) -> str:
        return self._data[ItemData].name

    @property
    def image(self) -> str:
        return self._data[ItemData].image

    @property
    def url(self) -> str:
        return "https://ddragon.leagueoflegends.com/cdn/{version}/img/item/{image}".format(
            version=ddragon["version"], image=self._data[ItemData].image,
        )

    @property
    def emoji(self) -> "EmojiObject":
        return self._data[ItemEmoji]

    @property
    def get_emoji(self) -> str:
        return self._data[ItemEmoji].get_emoji(self._data[ItemData].id)
