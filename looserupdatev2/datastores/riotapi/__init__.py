from typing import Dict
import os

from .common import RiotAPIService


def _default_services(
    api_key: str,
) -> Dict[RiotAPIService, str]:
    from riotwatcher import LolWatcher
    from .challenges import ChallengesApi
    from .championmastery import ChampionMasteryApi
    from .league import LeagueApi
    from .summoner import SummonerApi
    from .match import MatchApi

    client = LolWatcher(api_key)
    services = {
        "ChallengesAPI": ChallengesApi(
            api_key=api_key,
            client=client,
        ),
        "ChampionMasteryAPI": ChampionMasteryApi(
            api_key=api_key,
            client=client,
        ),
        "LeagueAPI": LeagueApi(
            api_key=api_key,
            client=client,
        ),
        "MatchAPI": MatchApi(
            api_key=api_key,
            client=client,
        ),
        "SummonerAPI": SummonerApi(
            api_key=api_key,
            client=client,
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
