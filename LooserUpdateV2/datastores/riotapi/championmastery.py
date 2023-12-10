from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...dto.championmastery import (
    ChampionMasteryDto,
    ChampionMasteryListDto,
    ChampionMasteryScoreDto,
)

_service = "champion_mastery"


class ChampionMasteryApi(RiotAPIService):
    """
    CHAMPION-MASTERY-V4
    League of Legends
    """
    def get_champion_mastery_list(
        self, query: MutableMapping[str, Any]
    ) -> ChampionMasteryListDto:
        """
        Get specified number of top champion mastery entries sorted by number of
        champion points descending.

        :param dict query:  Query parameters for the request:
                            - platform:    Platform
                            - summoner.id: Encrypted summoner ID. Max length 63 characters.

        :return: List[ChampionMasteryDto]: This object contains a list of Champion
                                           Mastery information for player and champion
                                           combination.
        """
        champion_mastery_count = 3

        parameters = dict(
            platform=query["platform"].value.lower(), encryptedSummonerId=query["summoner.id"],
        )
        endpoint = "by_summoner"

        try:
            data = self._get(
                _service, endpoint, parameters,
            )
        except APIError as error:
            raise APINotFoundError(str(error)) from error

        return ChampionMasteryListDto(
            championMasteryList=data[:champion_mastery_count]
        )

    def get_champion_mastery_score(
        self, query: MutableMapping[str, Any]
    ) -> ChampionMasteryScoreDto:
        """
        Get a player's total champion mastery score, which is the sum of
        individual champion mastery levels.

        :param dict query:  query parameters for the request:
                            - platform:    Platform
                            - summoner.id: Encrypted summoner ID. Max length 63 characters.

        :return: ChampionMasteryScoreDto
        """
        parameters = dict(
            platform=query["platform"].value.lower(), encryptedSummonerId=query["summoner.id"],
        )
        endpoint = "scores_by_summoner"

        try:
            data = self._get(
                _service, endpoint, parameters,
            )
        except APIError as error:
            raise APINotFoundError(str(error)) from error

        return ChampionMasteryScoreDto(
            score=data
        )
