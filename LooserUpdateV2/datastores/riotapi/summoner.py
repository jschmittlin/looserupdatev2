from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...dto.summoner import SummonerDto

_service = "summoner"


class SummonerApi(RiotAPIService):
    """
    SUMMONER-V4
    League of Legends
    """
    def get_summoner(
        self, query: MutableMapping[str, Any],
    ) -> SummonerDto:
        """
        Get a Summoner

        :param dict query:  Query parameters for the request:
                            - platform:   Platform
                            - accountId:  Encrypted account ID. Max length 56 characters.
                            - (or) name:  Summoner name.
                            - (or) id:    Encrypted summoner ID. Max length 63 characters.
                            - (or) puuid: Encrypted PUUID. Exact length of 78 characters.

        :return: SummonerDTO: represents a summoner        
        """
        if "accountId" in query:
            parameters = dict(
                platform=query["platform"].value.lower(), encryptedAccountId=query["accountId"],
            )
            endpoint = "by_account"
        elif "name" in query:
            parameters = dict(
                platform=query["platform"].value.lower(), summonerName=query["name"],
            )
            endpoint = "by_name"
        elif "id" in query:
            parameters = dict(
                platform=query["platform"].value.lower(), encryptedSummonerId=query["id"],
            )
            endpoint = "by_id"
        elif "puuid" in query:
            parameters = dict(
                platform=query["platform"].value.lower(), encryptedPUUID1=query["puuid"],
            )
            endpoint = "by_puuid"
        else:
            endpoint = ""

        try:
            data = self._get(
                _service, endpoint, parameters,
            )
        except APIError as error:
            raise APINotFoundError(str(error)) from error

        return SummonerDto(**data)
