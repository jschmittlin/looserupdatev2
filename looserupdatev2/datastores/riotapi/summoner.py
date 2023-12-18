from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...dto.summoner import SummonerDto


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
            url = "https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{encryptedAccountId}".format(
                platform=query["platform"].value.lower(), encryptedAccountId=query["accountId"],
            )
        if "name" in query:
            name = query["name"].replace(" ", "%20")
            url = "https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}".format(
                platform=query["platform"].value.lower(), summonerName=name,
            )
        if "puuid" in query:
            url = "https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}".format(
                platform=query["platform"].value.lower(), encryptedPUUID=query["puuid"],
            )
        if "id" in query:
            url = "https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/{encryptedSummonerId}".format(
                platform=query["platform"].value.lower(), encryptedSummonerId=query["id"],
            )

        try:
            data = self._get(url, {})
        except APINotFoundError as error:
            raise APINotFoundError(
                message=error.message, code=error.code, response_headers=error.response_headers
            )

        data["region"] = query["platform"].region.value
        return SummonerDto(data)
