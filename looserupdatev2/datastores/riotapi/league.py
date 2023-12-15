from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...dto.league import (
    LeagueEntryDto,
    LeagueEntriesDto,
)


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
                            - platform: Platform
                            - id:       Encrypted summoner ID. Max length 63 characters.

        :return: LeagueEntriesDTO
        """
        url = "https://{platform}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}".format(
            platform=query["platform"].value.lower(), encryptedSummonerId=query["id"],
        )

        try:
            data = self._get(url, {})
        except APINotFoundError as error:
            data = []

        region = query["platform"].region.value
        for entry in data:
            entry["region"] = region

        data = {
            "entries": data,
            "region": region,
            "summonerId": query["id"],
        }

        return LeagueEntriesDto(data)
