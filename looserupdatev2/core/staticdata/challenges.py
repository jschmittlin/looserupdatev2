from ..common import (
    CoreData,
    LolObject,
    ddragon,
)
from ...data import ChallengesTier
from ...dto.staticdata import challenges as dto


##############
# Data Types #
##############


class ChallengeTitleData(CoreData):
    _dto_type = dto.ChallengeTitleDto
    _renamed = {}


##############
# Core Types #
##############


class ChallengeTitle(LolObject):
    _data_types = {ChallengeTitleData}

    def __init__(
        self, id: str = None,
    ):
        self._data = {_type: None for _type in self._data_types}
        results = {_type: {} for _type in self._data_types}

        if id is None or id == "":
            return

        title_id = int(id)

        if title_id == 1:
            for _type in self._data_types:
                results[_type] = {"id": 1, "title": "Apprentice"}
        else:
            tier = ChallengesTier.from_id(title_id % 10).value

            data = ddragon["cache"]["challenges.json"]

            for challenge in data:
                if challenge["id"] == int(str(title_id)[:-2]):
                    for _type in self._data_types:
                        results[_type] = {"id": title_id, "title": challenge['thresholds'][tier]['rewards'][0]['title']}
                    break

        for _type, insert_this in results.items():
            if self._data[_type] is not None:
                self._data[_type] = self._data[_type](**insert_this)
            else:
                self._data[_type] = _type(**insert_this)

    def __str__(self) -> str:
        id = "?"
        title = "?"
        if hasattr(self._data[ChallengeTitleData], "id"):
            id = self._data[ChallengeTitleData].id
        if hasattr(self._data[ChallengeTitleData], "title"):
            title = self._data[ChallengeTitleData].title
        return "ChallengeTitle(id={id} title={title})".format(
            id=id, title=title,
        )

    @property
    def id(self) -> int:
        return self._data[ChallengeTitleData].id

    @property
    def title(self) -> str:
        if hasattr(self._data[ChallengeTitleData], "title"):
            return self._data[ChallengeTitleData].title
