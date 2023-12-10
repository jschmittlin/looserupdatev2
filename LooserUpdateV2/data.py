from typing import Dict
from enum import Enum

from .resources import (
    Icon,
    Color,
    emoji as Emoji
)


class Region(Enum):
    brazil = "BR"
    europe_north_east = "EUNE"
    europe_west = "EUW"
    japan = "JP"
    korea = "KR"
    latin_america_north = "LAN"
    latin_america_south = "LAS"
    north_america = "NA"
    oceania = "OCE"
    turkey = "TR"
    russia = "RU"
    philippines = "PH"
    singapore = "SG"
    thailand = "TH"
    taiwan = "TW"
    vietnam = "VN"

    def __str__(self) -> str:
        return "{} #{}".format(self.name.replace('_', ' ').title(), self.value)

    @property
    def platform(self) -> "Platform":
        return getattr(Platform, self.name)

    @property
    def icon(self) -> "Icon":
        return REGION_ICONS.get(self, Icon.transfer)

    @staticmethod
    def from_platform(platform) -> "Region":
        try:
            return platform.region
        except AttributeError:
            if isinstance(platform, str):
                return Platform(platform).region

REGION_ICONS = {
    Region.brazil: Icon.bresil,
    Region.europe_north_east: Icon.europe_north_east,
    Region.europe_west: Icon.europe_west,
    Region.japan: Icon.japan,
    Region.latin_america_north: Icon.latin_america_north,
    Region.latin_america_south: Icon.latin_america_south,
    Region.north_america: Icon.north_america,
    Region.oceania: Icon.oceania,
    Region.russia: Icon.russia,
    Region.turkey: Icon.turkey,
}


class Platform(Enum):
    brazil = "BR1"
    europe_north_east = "EUN1"
    europe_west = "EUW1"
    japan = "JP1"
    korea = "KR"
    latin_america_north = "LA1"
    latin_america_south = "LA2"
    north_america = "NA1"
    oceania = "OC1"
    turkey = "TR1"
    russia = "RU"
    philippines = "PH2"
    singapore = "SG2"
    thailand = "TH2"
    taiwan = "TW2"
    vietnam = "VN2"

    def __str__(self) -> str:
        return self.value

    @property
    def region(self) -> "Region":
        return getattr(Region, self.name)

    @staticmethod
    def from_region(region) -> "Platform":
        try:
            return region.platform
        except AttributeError:
            if isinstance(region, str):
                return Region(region).platform


class Lane(Enum):
    top = "Top"
    jungle = "Jungle"
    middle = "Mid"
    bottom = "ADC"
    utility = "Support"
    fill = "Fill"
    unselected = ""

    def __str__(self) -> str:
        return self.value

    @property
    def emoji(self) -> "Emoji":
        return LANE_EMOJIS[self]

    @property
    def emoji_hover(self) -> "Emoji":
        return LANE_EMOJIS_HOVER[self]

    def from_match_naming_scheme(string: str) -> "Lane":
        return {
            "TOP": Lane.top,
            "JUNGLE": Lane.jungle,
            "MIDDLE": Lane.middle,
            "BOTTOM": Lane.bottom,
            "UTILITY": Lane.utility,
            "NONE": Lane.unselected,
        }.get(string, Lane.unselected)

LANE_EMOJIS = {
    Lane.top: Emoji.Position.top,
    Lane.jungle: Emoji.Position.jungle,
    Lane.middle: Emoji.Position.mid,
    Lane.bottom: Emoji.Position.bottom,
    Lane.utility: Emoji.Position.utility,
    Lane.fill: Emoji.Position.fill,
    Lane.unselected: Emoji.Position.unselected,
}

LANE_EMOJIS_HOVER = {
    Lane.top: Emoji.Position.top_hover,
    Lane.jungle: Emoji.Position.jungle_hover,
    Lane.middle: Emoji.Position.mid_hover,
    Lane.bottom: Emoji.Position.bottom_hover,
    Lane.utility: Emoji.Position.utility_hover,
    Lane.fill: Emoji.Position.fill_hover,
    Lane.unselected: Emoji.Position.unselected_hover,
}


class Role(Enum):
    solo = "SOLO"
    duo = "DUO"
    duo_carry = "DUO_CARRY"
    duo_support = "DUO_SUPPORT"
    support = "SUPPORT"

    def from_match_naming_scheme(string: str) -> "Role":
        return {
            "SOLO": Role.solo,
            "DUO": Role.duo,
            "DUO_CARRY": Role.duo_carry,
            "DUO_SUPPORT": Role.duo_support,
            "SUPPORT": Role.support,
            "NONE": None,
        }.get(string, None)


class ChallengesTier(Enum):
    challenger = "CHALLENGER"
    grandmaster = "GRANDMASTER"
    master = "MASTER"
    diamond = "DIAMOND"
    platinum = "PLATINUM"
    gold = "GOLD"
    silver = "SILVER"
    bronze = "BRONZE"
    iron = "IRON"

    def from_id(id: int) -> "ChallengesTier":
        return {i: tier for tier, i in CHALLENGES_IDS.items()}[id]

CHALLENGES_IDS = {
    ChallengesTier.challenger: 8,
    ChallengesTier.grandmaster: 7,
    ChallengesTier.master: 6,
    ChallengesTier.diamond: 5,
    ChallengesTier.platinum: 4,
    ChallengesTier.gold: 3,
    ChallengesTier.silver: 2,
    ChallengesTier.bronze: 1,
    ChallengesTier.iron: 0,
}


class Tier(Enum):
    challenger = "CHALLENGER"
    grandmaster = "GRANDMASTER"
    master = "MASTER"
    diamond = "DIAMOND"
    emerald = "EMERALD"
    platinum = "PLATINUM"
    gold = "GOLD"
    silver = "SILVER"
    bronze = "BRONZE"
    iron = "IRON"
    unranked = "UNRANKED"

    def __str__(self) -> str:
        return self.name.title()

    @property
    def emoji(self) -> "Emoji":
        return TIER_EMOJIS[self]

    @property
    def color(self) -> "Color":
        return TIER_COLORS[self]

    @staticmethod
    def _order() -> Dict["Tier", int]:
        return {
            Tier.challenger: 10,
            Tier.grandmaster: 9,
            Tier.master: 8,
            Tier.diamond: 7,
            Tier.emerald: 6,
            Tier.platinum: 5,
            Tier.gold: 4,
            Tier.silver: 3,
            Tier.bronze: 2,
            Tier.iron: 1,
            Tier.unranked: 0,
        }

    def __lt__(self, other) -> bool:
        return self._order()[self] < self._order()[other]

    def __gt__(self, other) -> bool:
        return self._order()[self] > self._order()[other]

    def __le__(self, other) -> bool:
        return self._order()[self] <= self._order()[other]

    def __ge__(self, other) -> bool:
        return self._order()[self] >= self._order()[other]

TIER_EMOJIS = {
    Tier.challenger: Emoji.Ranked.challenger,
    Tier.grandmaster: Emoji.Ranked.grandmaster,
    Tier.master: Emoji.Ranked.master,
    Tier.diamond: Emoji.Ranked.diamond,
    Tier.emerald: Emoji.Ranked.emerald,
    Tier.platinum: Emoji.Ranked.platinum,
    Tier.gold: Emoji.Ranked.gold,
    Tier.silver: Emoji.Ranked.silver,
    Tier.bronze: Emoji.Ranked.bronze,
    Tier.iron: Emoji.Ranked.iron,
    Tier.unranked: Emoji.Ranked.unranked,
}

TIER_COLORS = {
    Tier.challenger: Color.ansi_blue,
    Tier.grandmaster: Color.ansi_red,
    Tier.master: Color.ansi_pink,
    Tier.diamond: Color.ansi_cyan,
    Tier.emerald: Color.ansi_green,
    Tier.platinum: Color.ansi_cyan,
    Tier.gold: Color.ansi_yellow,
    Tier.silver: Color.ansi_white,
    Tier.bronze: Color.ansi_reset,
    Tier.iron: Color.ansi_gray,
    Tier.unranked: Color.ansi_gray,
}


class Division(Enum):
    one = "I"
    two = "II"
    three = "III"
    four = "IV"

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def _order() -> Dict["Division", int]:
        return {
            Division.one: 4,
            Division.two: 3,
            Division.three: 2,
            Division.four: 1,
        }

    def __lt__(self, other) -> bool:
        return self._order()[self] < self._order()[other]

    def __gt__(self, other) -> bool:
        return self._order()[self] > self._order()[other]

    def __le__(self, other) -> bool:
        return self._order()[self] <= self._order()[other]

    def __ge__(self, other) -> bool:
        return self._order()[self] >= self._order()[other]


class Rank:
    def __init__(self, tier: Tier, division: Division):
        self.tuple = (tier, division)
        self.tier = tier
        self.division = division

    def __str__(self) -> str:
        return "<{} {}>".format(self.tuple[0], self.tuple[1])

    def __eq__(self, other) -> bool:
        return self.tuple == other.tuple

    def __ne__(self, other) -> bool:
        return self.tuple != other.tuple

    def __lt__(self, other) -> bool:
        return self.tuple < other.tuple

    def __gt__(self, other) -> bool:
        return self.tuple > other.tuple

    def __le__(self, other) -> bool:
        return self.tuple <= other.tuple

    def __ge__(self, other) -> bool:
        return self.tuple >= other.tuple


class MatchType(Enum):
    ranked = "ranked"
    normal = "normal"
    tourney = "tourney"
    tutorial = "tutorial"


# References for game modes:
# https://static.developer.riotgames.com/docs/lol/gameModes.json
class GameMode(Enum):
    classic = "CLASSIC"
    dominion = "ODIN"
    aram = "ARAM"
    tutorial = "TUTORIAL"
    urf = "URF"
    doom_bots = "DOOMBOTSTEEMO"
    one_for_all = "ONEFORALL"
    ascension = "ASCENSION"
    showdown = "FIRSTBLOOD"
    poro_king = "KINGPORO"
    nexus_siege = "SIEGE"
    blood_hunt = "ASSASSINATE"
    all_random_summoners_rift = "ARSR"
    dark_star = "DARKSTAR"
    star_guardian = "STARGUARDIAN"
    project = "PROJECT"
    odysssey = "ODYSSEY"
    nexus_blitz = "NEXUSBLITZ"
    ultbook = "ULTBOOK"


# References for game types:
# https://static.developer.riotgames.com/docs/lol/gameTypes.json
class GameType(Enum):
    custom = "CUSTOM_GAME"
    tutorial = "TUTORIAL_GAME"
    matchmade = "MATCHED_GAME"


# References for queues:
# https://static.developer.riotgames.com/docs/lol/queues.json
class Queue(Enum):
    custom = "CUSTOM"
    normal_draft_five = "NORMAL_5x5_DRAFT"
    ranked_solo_five = "RANKED_SOLO_5x5"
    ranked_flex_five = "RANKED_FLEX_SR"
    aram = "ARAM"
    cherry = "ARENA"

    def from_id(id: int) -> "Queue":
        return {i: queue for queue, i in QUEUE_IDS.items()}[id]

    @property
    def id(self) -> int:
        return QUEUE_IDS[self]

    @property
    def map(self) -> str:
        return QUEUE_MAPS[self]

    @property
    def description(self) -> str:
        return QUEUE_DESCRIPTIONS[self]

    @property
    def icon_victory(self) -> "Icon":
        return QUEUE_MAPS_ICONS_VICTORY.get(self, Icon.classic_victory)

    @property
    def icon_defeat(self) -> "Icon":
        return QUEUE_MAPS_ICONS_DEFEAT.get(self, Icon.classic_defeat)

    @property
    def emoji_victory(self) -> "Emoji":
        return QUEUE_MAPS_EMOJIS_VICTORY.get(self, Emoji.GameMode.rgm_victory)

    @property
    def emoji_defeat(self) -> "Emoji":
        return QUEUE_MAPS_EMOJIS_DEFEAT.get(self, Emoji.GameMode.rgm_defeat)

QUEUE_IDS = {
    Queue.custom: 0,
    Queue.normal_draft_five: 400,
    Queue.ranked_solo_five: 420,
    Queue.ranked_flex_five: 440,
    Queue.aram: 450,
    Queue.cherry: 1700,
}

QUEUE_MAPS = {
    Queue.custom: "Custom",
    Queue.normal_draft_five: "Summoner's Rift",
    Queue.ranked_solo_five: "Summoner's Rift",
    Queue.ranked_flex_five: "Summoner's Rift",
    Queue.aram: "Howling Abyss",
    Queue.cherry: "Rings of Wrath",
}

QUEUE_DESCRIPTIONS = {
    Queue.custom: "Custom",
    Queue.normal_draft_five: "Normal (Draft Pick)",
    Queue.ranked_solo_five: "Ranked Solo/Duo",
    Queue.ranked_flex_five: "Ranked Flex",
    Queue.aram: "ARAM",
    Queue.cherry: "Arena",
}

QUEUE_MAPS_ICONS_VICTORY = {
    Queue.normal_draft_five: Icon.classic_victory,
    Queue.ranked_solo_five: Icon.classic_victory,
    Queue.ranked_flex_five: Icon.classic_victory,
    Queue.aram: Icon.aram_victory,
    Queue.cherry: Icon.cherry_victory,
}

QUEUE_MAPS_ICONS_DEFEAT = {
    Queue.normal_draft_five: Icon.classic_defeat,
    Queue.ranked_solo_five: Icon.classic_defeat,
    Queue.ranked_flex_five: Icon.classic_defeat,
    Queue.aram: Icon.aram_defeat,
    Queue.cherry: Icon.cherry_defeat,
}

QUEUE_MAPS_EMOJIS_VICTORY = {
    Queue.normal_draft_five: Emoji.GameMode.classic_victory,
    Queue.ranked_solo_five: Emoji.GameMode.classic_victory,
    Queue.ranked_flex_five: Emoji.GameMode.classic_victory,
    Queue.aram: Emoji.GameMode.aram_victory,
    Queue.cherry: Emoji.GameMode.cherry_victory,
}

QUEUE_MAPS_EMOJIS_DEFEAT = {
    Queue.normal_draft_five: Emoji.GameMode.classic_defeat,
    Queue.ranked_solo_five: Emoji.GameMode.classic_defeat,
    Queue.ranked_flex_five: Emoji.GameMode.classic_defeat,
    Queue.aram: Emoji.GameMode.aram_defeat,
    Queue.cherry: Emoji.GameMode.cherry_defeat,
}
