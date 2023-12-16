from typing import Dict
import os

from .common import RiotAPIService


def _default_services(
    api_key: str,
) -> Dict[RiotAPIService, str]:
    from ..common import HTTPClient
    from .account import AccountApi
    from .challenges import ChallengesApi
    from .championmastery import ChampionMasteryApi
    from .league import LeagueApi
    from .match import MatchApi
    from .summoner import SummonerApi

    client = HTTPClient()
    services = {
        "AccountAPI": AccountApi(
            api_key=api_key,
            http_client=client,
        ),
        "ChallengesAPI": ChallengesApi(
            api_key=api_key,
            http_client=client,
        ),
        "ChampionMasteryAPI": ChampionMasteryApi(
            api_key=api_key,
            http_client=client,
        ),
        "LeagueAPI": LeagueApi(
            api_key=api_key,
            http_client=client,
        ),
        "MatchAPI": MatchApi(
            api_key=api_key,
            http_client=client,
        ),
        "SummonerAPI": SummonerApi(
            api_key=api_key,
            http_client=client,
        ),
    }

    return services

class RiotAPI:
    def __init__(
        self,
        api_key: str = None,
        services: Dict[RiotAPIService, str] = None,
    ) -> None:
        if api_key is None:
            api_key = "RIOT_API_KEY"
        if not api_key.startswith("RGAPI"):
            api_key = os.environ.get(api_key, None)

        if services is None:
            self.services = _default_services(
                api_key=api_key,
            )
