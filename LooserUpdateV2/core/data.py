from enum import Enum
from discord import app_commands

from datastores.ddragon import DDragon

class Region(Enum):
    brazil              = ["BR", "BRAZIL"]
    europe_north_east   = ["EUNE", "EUROPE NORTH EAST"]
    europe_west         = ["EUW", "EUROPE WEST"]
    japan               = ["JP", "JAPAN"]
    korea               = ["KR", "KOREA"]
    latin_america_north = ["LAN", "LATIN AMERICA NORTH"]
    latin_america_south = ["LAS", "LATIN AMERICA SOUTH"]
    north_america       = ["NA", "NORTH AMERICA"]
    oceania             = ["OCE", "OCEANIA"]
    turkey              = ["TR", "TURKEY"]
    russia              = ["RU", "RUSSIA"]
    philippines         = ["PH", "PHILIPPINES"]
    singapore           = ["SG", "SINGAPORE"]
    thailand            = ["TH", "THAILAND"]
    taiwan              = ["TW", "TAIWAN"]
    vietnam             = ["VN", "VIETNAM"]
    
    def __str__(self) -> str:
        return f"{self.value[1].capitalize()} ({self.value[0]})"

    @property
    def platform(self) -> "Platform":
        return getattr(Platform, self.name)

    @staticmethod
    def from_platform(region: str) -> platform:
        try:
            for i in Region:
                if region.upper() in i.value:
                    return i.platform
        except:
            return None

    @staticmethod
    def get_choices() -> list:
        return [app_commands.Choice(name=str(i), value=i.value[0]) for i in Region]

class Platform(Enum):
    brazil              = "BR1"
    europe_north_east   = "EUN1"
    europe_west         = "EUW1"
    japan               = "JP1"
    korea               = "KR"
    latin_america_north = "LA1"
    latin_america_south = "LA2"
    north_america       = "NA1"
    oceania             = "OC1"
    turkey              = "TR1"
    russia              = "RU"
    philippines         = "PH2"
    singapore           = "SG2"
    thailand            = "TH2"
    taiwan              = "TW2"
    vietnam             = "VN2"

    def __str__(self) -> str:
        return self.value
        
    @property
    def region(self) -> "Region":
        return getattr(Region, self.name)

    @staticmethod
    def from_region(region: str) -> Region:
        try:
            return region.platform
        except AttributeError:
            return Platform(region).region


class Champion():
    @staticmethod
    def from_id(id: int):
        try:
            data = DDragon.get_champion()
            for champion in data:
                if data[champion]['key'] == str(id):
                    name = data[champion]['name']
                    return Champion.fix_name(name)
        except Exception as error:
            return error

    @staticmethod
    def fix_name(string: str):
        return FIX_NAMES.get(string, string)
    
FIX_NAMES = {
    "AurelionSol":  "Aurelion Sol",
    "Belveth":      "Bel'veth",
    "Chogath":      "Cho'Gath",
    "DrMundo":      "Dr. Mundo",
    "Fiddlesticks": "FiddleSticks",
    "JarvanIV":     "Jarvan IV",
    "Kaisa":        "Kai'Sa",
    "Khazix":       "Kha'Zix",
    "KogMaw":       "Kog'Maw",
    "KSante":       "K'Sante",
    "Leblanc":      "LeBlanc",
    "LeeSin":       "Lee Sin",
    "MasterYi":     "Master Yi",
    "MissFortune":  "Miss Fortune",
    "MonkeyKing":   "Wukong",
    "Nunu":         "Nunu & Willump",
    "RekSai":       "Rek'Sai",
    "TahmKench":    "Tahm Kench",
    "TwistedFate":  "Twisted Fate",
    "Velkoz":       "Vel'Koz",
    "XinZhao":      "Xin Zhao",
}

class Challenges():
    @staticmethod
    def from_id(id: int):
        try:
            challenge_id = int(id[:-2])
            tier_id = CHALLENGES_TIER_IDS[int(id[-1])]
            data = DDragon.get_challenges()
            for challenge in data:
                if challenge['id'] == challenge_id:
                    return challenge['thresholds'][tier_id]['rewards'][0]['title']
        except:
            return None

CHALLENGES_TIER_IDS = {
    0: "IRON",
    1: "BRONZE",
    2: "SILVER",
    3: "GOLD",
    4: "PLATINUM",
    5: "DIAMOND",
    6: "MASTER",
    7: "GRANDMASTER",
    8: "CHALLENGER",
}

class Queue():
    map = None
    description = None

    @staticmethod
    def from_id(id: int):
        try:
            data = DDragon.get_queues()
            for queue in data:
                if queue['queueId'] == id:
                    Queue.map = queue['map']
                    Queue.description = Queue.filter(queue['description'])
        except:
            pass

    @staticmethod
    def filter(string: str) -> str:
        replacements = {
            " games":       "",
            "5v5 ":         "",
            "3v3 ":         "",
            "Solo":         "Solo/Duo",
            "Pick URF":     "Ultra Rapid Fire",
            "Draft Pick":   "Normal (Draft Pick)",
            "Co-op vs. AI": "",
            "Bot":          "",
        }
        for old, new in replacements.items():
            string = string.replace(old, new)
        return string
        

class Rune(Enum):
    arcane_comet            = "Arcane Comet"
    conqueror               = "Conqueror"
    dark_harvest            = "Dark Harvest"
    electrocute             = "Electrocute"
    first_strike            = "First Blood"
    fleet_footwork          = "Fleet Footwork"
    glacial_augment         = "Glacial Augment"
    grasp_of_the_undying    = "Grasp of the Undying"
    guardian                = "Guardian"
    hail_of_blades          = "Hail of Blades"
    lethal_tempo            = "Lethal Tempo"
    phase_rush              = "Phase Rush"
    predator                = "Predator"
    press_the_attack        = "Press the Attack"
    summon_aery             = "Summon Aery"
    unsealed_spellbook      = "Unsealed Spellbook"
    aftershock              = "Aftershock"
    none                    = "None"

    @staticmethod
    def from_league(string: str):
        return Rune.get(string.lower().replace(' ','_'), Rune.none)

class Summoner(Enum):
    barrier                 = "SummonerBarrier"
    boost                   = "SummonerBoost"
    dot                     = "SummonerDot"
    exhaust                 = "SummonerExhaust"
    flash                   = "SummonerFlash"
    haste                   = "SummonerHaste"
    heal                    = "SummonerHeal"
    mana                    = "SummonerMana"
    poroRecall              = "SummonerPoroRecall"
    poroThrow               = "SummonerPoroThrow"
    smite                   = "SummonerSmite"
    snowURFSnowball_Mark    = "SummonerSnowURFSnowball_Mark"
    snowball                = "SummonerSnowball"
    teleport                = "SummonerTeleport"
    ultBookPlaceholder      = "SummonerUltBookPlaceholder"
    ultBookSmitePlaceholder = "SummonerUltBookSmitePlaceholder"
    none                    = "None"

    @staticmethod
    def from_key(key: int):
        return {i: summoner for summoner, i in KEYS.items()}.get(key, Summoner.none)

    @property
    def key(self): 
        return KEYS.get(self, -1)

KEYS = {
    Summoner.barrier:                   21,
    Summoner.boost:                     1,
    Summoner.dot:                       14,
    Summoner.exhaust:                   3,
    Summoner.flash:                     4,
    Summoner.haste:                     6,
    Summoner.heal:                      7,
    Summoner.mana:                      13,
    Summoner.poroRecall:                30,
    Summoner.poroThrow:                 31,
    Summoner.smite:                     11,
    Summoner.snowURFSnowball_Mark:      39,
    Summoner.snowball:                  32,
    Summoner.teleport:                  12,
    Summoner.ultBookPlaceholder:        54,
    Summoner.ultBookSmitePlaceholder:   55,
    Summoner.none:                      -1,
}
        
