from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...data import Continent, MatchType, Queue, QUEUE_IDS
from ...dto.match import (
    MatchListDto,
    MatchDto,
)


class MatchApi(RiotAPIService):
    """
    MATCH-V5
    League of Legends
    """
    def get_match(
        self, query: MutableMapping[str, Any]
    ) -> MatchDto:
        """
        Get a match by match ID.

        :param dict query:  Query parameters for the request:
                            - platform: Platform
                            - id:       Match ID

        :return: MatchDto
        """
        platform = query["platform"]
        continent: Continent = platform.continent
        id = query["id"]
        url = "https://{continent}.api.riotgames.com/lol/match/v5/matches/{platform}_{id}".format(
            continent=continent.value.lower(), platform=platform.value, id=id,
        )
        try:
            data = self._get(url, {})
            data = data["info"]
        except APINotFoundError as error:
            raise APINotFoundError(str(error)) from error

        data["region"] = platform.region.value
        data["matchId"] = id
        return MatchDto(data)

    def get_match_list(
        self, query: MutableMapping[str, Any]
    ) -> MatchListDto:
        """
        Get a list of match IDs by PUUID.

        :param dict query:  Query parameters for the request:
                            - region:           Region
                            - puuid:            Encrypted summoner ID. Max length 63 characters.
                            - (optional) queue: Filter the list of match ids by the queue ids
                                                This filter is mutually inclusive of the type filter
                                                meaning any match ids returned must match both the
                                                queue and type filters.
                            - (optional) type:  Filter the list of match ids by the type of match.
                                                This filter is mutually inclusive of the queue filter
                                                meaning any match ids returned must match both the
                                                queue and type filters.
                            - (optional) start: Defaults to 0. Start index.
                            - (optional) count: Defaults to 20. Valid values: 0 to 100. Number of
                                                matches to return.

        :return: List[string]
        """
        parameters = {}

        riot_max_interval = 100

        start = query.get("start", 0)
        parameters["start"] = start

        count = query.get("count", 20)
        parameters["count"] = int(min(riot_max_interval, count))

        queue = query.get("queue", None)
        if queue is not None:
            parameters["queue"] = QUEUE_IDS[queue]

        type = query.get("type", None)
        if type is not None:
            parameters["type"] = MatchType(type).value   

        continent: Continent = query["region"].continent
        puuid: str = query["puuid"]
        url = "https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids".format(
            continent=continent.value.lower(), puuid=puuid,
        )

        try:
            data = self._get(url, parameters)
            data = [id.split("_")[1] for id in data]
        except APINotFoundError as error:
            data = []

        data = {
            "match_ids": data,
            "region": query["region"].value,
            "puuid": puuid,
            "queue": queue,
            "type": type,
            "start": start,
            "count": parameters["count"],
        }

        return MatchListDto(data)
