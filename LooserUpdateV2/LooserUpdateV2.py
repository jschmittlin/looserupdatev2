from typing import Union

from .data import Region, Platform, Queue, MatchType, Tier, Division
from .core import (
    ChallengeTitle,
    Champion,
    ChampionMasteries,
    Item,
    LeagueEntries,
    Match,
    MatchHistory,
    PlayerInfo,
    Player,
    PlayerList,
    ProfileIcon,
    Rune,
    Summoner,
    SummonerSpell,
)


def get_summoner(
    *,
    id: str = None,
    account_id: str = None,
    puuid: str = None,
    name: str = None,
    region: Union[Region, str] = None,
) -> Summoner:
    return Summoner(id=id, account_id=account_id, puuid=puuid, name=name, region=region)

def get_league_entries(summoner: Summoner) -> LeagueEntries:
    return LeagueEntries(summoner=summoner)

def get_champion_masteries(summoner: Summoner) -> ChampionMasteries:
    return ChampionMasteries(summoner=summoner)

def get_challenge(summoner: Summoner) -> PlayerInfo:
    return PlayerInfo(summoner=summoner)

def get_match_history(
    region: Union[Region, str] = None,
    puuid: str = None,
    queue: Queue = None,
    type: MatchType = None,
    start: int = None,
    count: int = None,
) -> MatchHistory:
    return MatchHistory(region=region, puuid=puuid, queue=queue, type=type, start=start, count=count)

def get_match(region: Union[Region, str] = None, id: int = None) -> Match:
    return Match(region=region, id=id)

def get_champion(*, id: str = None, name: str = None, key: str = None) -> Champion:
    return Champion(id=id, name=name, key=key)

def get_profile_icon(id: int = None) -> ProfileIcon:
    return ProfileIcon(id=id)

def get_challenge_title(id: int = None) -> ChallengeTitle:
    return ChallengeTitle(id=id)

def get_item(id: int = None) -> Item:
    return Item(id=id)

def get_rune(id: int = None) -> Rune:
    return Rune(id=id)

def get_summoner_spell(key: int = None) -> SummonerSpell:
    return SummonerSpell(key=key)

def get_player_list() -> PlayerList:
    return PlayerList()

def get_player(name: str) -> Player:
    return PlayerList().get(name=name)

def add_player(summoner: Summoner) -> Player:
    return PlayerList().add(summoner=summoner)

def remove_player(name: str) -> Player:
    return PlayerList().remove(name=name)
