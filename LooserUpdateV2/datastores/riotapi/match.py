from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...data import MatchType, Queue, QUEUE_IDS
from ...dto.match import (
    MatchListDto,
    MatchDto,
)

_service = "match"


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
                            - match.id: Match ID

        :return: MatchDto
        """
        parameters = dict(
            platform=query["platform"].value.lower(), matchId=query["match.id"],
        )
        endpoint = "by_id"

        try:
            data = self._get(
                _service, endpoint, parameters,
            )
        except APIError as error:
            raise APINotFoundError(str(error)) from error

        return MatchDto(**data)

    def get_match_list(
        self, query: MutableMapping[str, Any]
    ) -> MatchListDto:
        """
        Get a list of match IDs by PUUID.

        :param dict query:      Query parameters for the request:
                                - platform:         Platform
                                - summoner.puuid:   Encrypted summoner ID. Max length 63 characters.
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

        start = query["start"]
        parameters["start"] = start

        count = query["count"]
        parameters["count"] = int(min(riot_max_interval, count))

        queue = query.get("queue", None)
        if queue is not None:
            parameters["queue"] = QUEUE_IDS[queue]

        type = query.get("type", None)
        if type is not None:
            parameters["type"] = MatchType(type).value   

        puuid = query["summoner.puuid"]
        parameters["encryptedPUUID2"] = puuid

        platform = query["platform"]
        parameters["platform"] = platform.value.lower()

        endpoint = "matchlist_by_puuid"

        try:
            data = self._get(
                _service, endpoint, parameters,
            )
        except APIError as error:
            raise APINotFoundError(str(error)) from error

        return MatchListDto(
            match_ids=data, puuid=puuid, queue=queue, type=type, start=start, count=parameters["count"],
        )
