from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...dto.championmastery import (
    ChampionMasteryDto,
    ChampionMasteryListDto,
    ChampionMasteryScoreDto,
)


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
                            - platform: Platform
                            - puuid:    Encrypted PUUID. Exact length of 78 characters.
                            - (or) id:  Encrypted summoner ID. Max length 63 characters.

        :return: List[ChampionMasteryDto]
        """
        if "puuid" in query:
            url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/top".format(
                platform=query["platform"].value.lower(), encryptedPUUID=query["puuid"],
            )
        if "id" in query:
            url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}/top".format(
                platform=query["platform"].value.lower(), encryptedSummonerId=query["id"],
            )

        try:
            data = self._get(url, {})
        except APINotFoundError as error:
            raise APINotFoundError(
                message=error.message, code=error.code, response_headers=error.response_headers
            )

        data = {
            "championMasteryList": data,
            "region": query["platform"].region.value,
        }

        if "puuid" in query:
            data["puuid"] = query["puuid"]

        if "id" in query:
            data["id"] = query["id"]

        return ChampionMasteryListDto(data)

    def get_champion_mastery_score(
        self, query: MutableMapping[str, Any]
    ) -> ChampionMasteryScoreDto:
        """
        Get a player's total champion mastery score, which is the sum of
        individual champion mastery levels.

        :param dict query:  query parameters for the request:
                            - platform: Platform
                            - puuid:    Encrypted PUUID. Exact length of 78 characters.
                            - (or) id:  Encrypted summoner ID. Max length 63 characters.

        :return: ChampionMasteryScoreDto
        """
        if "puuid" in query:
            url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/scores/by-puuid/{encryptedPUUID}".format(
                platform=query["platform"].value.lower(), encryptedPUUID=query["puuid"],
            )
        if "id" in query:
            url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/{encryptedSummonerId}".format(
                platform=query["platform"].value.lower(), encryptedSummonerId=query["id"],
            )

        try:
            data = self._get(url, {})
        except APINotFoundError as error:
            raise APINotFoundError(
                message=error.message, code=error.code, response_headers=error.response_headers
            )

        data = {
            "score": data,
            "region": query["platform"].region.value,
        }

        if "puuid" in query:
            data["puuid"] = query["puuid"]

        if "id" in query:
            data["id"] = query["id"]

        return ChampionMasteryScoreDto(data)
