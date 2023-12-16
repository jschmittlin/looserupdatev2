from typing import Union, List

from .data import Region, Platform, Queue, MatchType, Tier, Division
from .core import (
    Account,
    Augment,
    ChallengeTitle,
    Champion,
    ChampionMasteries,
    Item,
    Items,
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


def get_account(
    *,
    puuid: str = None,
    game_name: str = None,
    tag_line: str = None,
    region: Union[Region, str] = None,
) -> Account:
    return Account(puuid=puuid, game_name=game_name, tag_line=tag_line, region=region)

def get_summoner(
    *,
    id: str = None,
    account_id: str = None,
    puuid: str = None,
    name: str = None,
    region: Union[Region, str] = None,
) -> Summoner:
    return Summoner(id=id, account_id=account_id, puuid=puuid, name=name, region=region)

def get_match_history(
    *,
    region: Union[Region, str] = None,
    puuid: str = None,
    queue: Queue = None,
    type: MatchType = None,
    start: int = None,
    count: int = None,
) -> MatchHistory:
    return MatchHistory(region=region, puuid=puuid, queue=queue, type=type, start=start, count=count)

def get_match(
    *,
    region: Union[Region, str] = None,
    platform: Union[Platform, str] = None,
    id: str = None
) -> Match:
    return Match(region=region, platform=platform, id=id)

def get_league_entries(summoner: Summoner) -> LeagueEntries:
    return LeagueEntries(summoner=summoner)

def get_champion_masteries(summoner: Summoner) -> ChampionMasteries:
    return ChampionMasteries(summoner=summoner)

def get_challenges(summoner: Summoner) -> PlayerInfo:
    return PlayerInfo(summoner=summoner)

def get_champion(
    *,
    id: str = None,
    name: str = None,
    key: str = None
) -> Champion:
    return Champion(id=id, name=name, key=key)

def get_item(
    *,
    id: str = None,
    name: str = None,
    image: str = None,
) -> Item:
    return Item(id=id, name=name, image=image)

def get_items(included_data: List[str] = None) -> Items:
    return Items(included_data=included_data)

def get_summoner_spell(
    *,
    id: str = None,
    key: str = None,
) -> SummonerSpell:
    return SummonerSpell(id=id, key=key)

def get_augment(id: int = None) -> Augment:
    return Augment(id=id)

def get_profile_icon(id: int = None) -> ProfileIcon:
    return ProfileIcon(id=id)

def get_challenge_title(id: int = None) -> ChallengeTitle:
    return ChallengeTitle(id=id)

def get_rune(id: int = None) -> Rune:
    return Rune(id=id)

def get_player_list() -> PlayerList:
    return PlayerList()

def get_player(game_name: str = None, tag_line: str = None) -> Player:
    return PlayerList().get(name=name)

def add_player(summoner: Summoner) -> Player:
    return PlayerList().add(summoner=summoner)

def remove_player(game_name: str = None, tag_line: str = None) -> Player:
    return PlayerList().remove(name=name)
