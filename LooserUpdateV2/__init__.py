from .configuration import (
    get_default_config,
    Settings,
    LooserUpdateV2Configuration as _LooserUpdateV2Configuration,
)

configuration = _LooserUpdateV2Configuration()

from .looserupdatev2 import (
    get_challenge,
    get_challenge_title,
    get_champion,
    get_champion_masteries,
    get_item,
    get_league_entries,
    get_match,
    get_match_history,
    get_profile_icon,
    get_rune,
    get_summoner,
    get_summoner_spell,
)
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
from .data import (
    Division,
    GameMode,
    GameType,
    Lane,
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
)
from .resources import (
    Color,
    Icon,
    GameMode,
    Mastery,
    Match,
    Position,
    Ranked,
)
