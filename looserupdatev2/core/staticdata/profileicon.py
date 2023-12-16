from ..common import (
    CoreData,
    LolObject,
    ddragon,
)
from ...dto.staticdata import profileicon as dto


##############
# Data Types #
##############


class ProfileIconData(CoreData):
    _dto_type = dto.ProfileIconDto
    _renamed = {}


##############
# Core Types #
##############


class ProfileIcon(LolObject):
    _data_types = {ProfileIconData}

    def __init__(
        self, id: int = None,
    ):
        kwargs = {}
        if id is not None:
            kwargs["id"] = id
        super().__init__(**kwargs)

    def __str__(self) -> str:
        id = "?"
        if hasattr(self._data[ProfileIconData], "id"):
            id = self._data[ProfileIconData].id
        return "ProfileIcon(id={id})".format(
            id=id,
        )

    @property
    def id(self) -> int:
        return self._data[ProfileIconData].id

    @property
    def url(self) -> str:
        return "https://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{id}.png".format(
            version=ddragon["version"], id=self._data[ProfileIconData].id,
        )
