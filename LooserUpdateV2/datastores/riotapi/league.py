from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...dto.league import (
    LeagueEntryDto,
    LeagueEntriesDto,
)

_service = "league"


class LeagueApi(RiotAPIService):
    """
    LEAGUE-V4
    League of Legends
    """
    def get_league_entries_by_summoner(
        self, query: MutableMapping[str, Any]
    ) -> LeagueEntriesDto:
        """
        Get league entries in all queues for a given summoner ID.

        :param dict query:  Query parameters for the request:
                            - platform:    Platform
                            - summoner.id: Encrypted summoner ID. Max length 63 characters.

        :return: LeagueEntriesDTO
        """
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

        return LeagueEntriesDto(
            entries=data
        )
