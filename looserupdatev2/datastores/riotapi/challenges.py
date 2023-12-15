from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...dto.challenges import PlayerInfoDto


class ChallengesApi(RiotAPIService):
    """
    LOL-CHALLENGES-V1
    League of Legends
    """
    def get_player_data(
        self, query: MutableMapping[str, Any]
    ) -> PlayerInfoDto:
        """
        Get player information with list of all progressed challenges.

        :param dict query:  Query parameters for the request:
                            - platform: Platform
                            - puuid:    Encrypted summoner ID. Max length 63 characters.

        :return: PlayerInfoDTO:
        """
        url = "https://{platform}.api.riotgames.com/lol/challenges/v1/player-data/{puuid}".format(
            platform=query["platform"].value.lower(), puuid=query["puuid"],
        )

        try:
            data = self._get(url, {})
        except APINotFoundError as error:
            raise APINotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return PlayerInfoDto(data)
