from .configuration import (
    get_default_config,
    Settings,
    LooserUpdateV2Configuration as _LooserUpdateV2Configuration,
)

configuration = _LooserUpdateV2Configuration()

from .looserupdatev2 import (
    get_account,
    get_augment,
    get_challenge_title,
    get_challenges,
    get_champion_masteries,
    get_champion,
    get_items,
    get_item,
    get_league_entries,
    get_match_history,
    get_match,
    get_profile_icon,
    get_rune,
    get_summoner_spell,
    get_summoner,
    get_player_list,
    get_player,
    add_player,
    remove_player,
)
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
from .data import (
    ChallengesTier,
    Continent,
    Division,
    GameMode,
    GameType,
    Lane,
    MatchType,
    Platform,
    Queue,
    Rank,
    Region,
    Role,
    Tier,
)

from .core import (
    LooserUpdateV2Bot,
    Embed,
    ProfileView,
    UpdatePlayerView,
)
from .resources import (
    blank,
    Color,
    GameMode,
    Icon,
    Mastery,
    Match,
    Position,
    Ranked,
)
