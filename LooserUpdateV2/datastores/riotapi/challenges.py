from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...dto.challenges import PlayerInfoDto

_service = "challenges"


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

        :param dict query: Query parameters for the request:
                           - platform:       Platform
                           - summoner.puuid: Encrypted summoner ID. Max length 63 characters.

        :return: PlayerInfoDTO: Player information with list of all progressed challenges.
        """
        parameters = dict(
            platform=query["platform"].value.lower(), encryptedPUUID2=query["summoner.puuid"],
        )
        endpoint = "by_puuid"

        try:
            data = self._get(
                _service, endpoint, parameters,
            )
        except APIError as error:
            raise APINotFoundError(str(error)) from error

        return PlayerInfoDto(**data)
