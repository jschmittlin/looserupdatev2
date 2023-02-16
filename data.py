from enum import Enum
import json
import requests
from io import BytesIO

# Discord bot
import discord
from discord import app_commands

PATH = './data/'

# List of activities
ACTIVITIES = [
    discord.Activity(type=discord.ActivityType.watching, name="you"),
    discord.Activity(type=discord.ActivityType.watching, name="Medhi put pressure on"),
    discord.Activity(type=discord.ActivityType.watching, name="Medhi be shadow ban"),
    discord.Activity(type=discord.ActivityType.watching, name="botlane feed"),
    discord.Activity(type=discord.ActivityType.watching, name="Jérôme farmer these jungle camps"),
    discord.Activity(type=discord.ActivityType.listening, name="Valentin raging"),
    discord.Activity(type=discord.ActivityType.listening, name="La déprime"),
    discord.Game(name="for /help"),
    discord.Game(name="at tracking down losers"),
    discord.Game(name="Blitzcrank's Poro Roundup"),
    discord.Game(name="Doom Bots"),
    discord.Game(name="to support KCorp !"),
]

class Emoji:
    def __init__(self, bot):
        self.bot = bot

    async def create_emoji(self, server_id, name, url):
        response = requests.get(url)
        if response.status_code != 200:
            return False, 'Failed to get image from URL.'
        image_data = BytesIO(response.content)

        server = self.bot.get_guild(server_id)
        if server is None:
            return False, 'Invalid server ID.'

        emoji_data = image_data.read()

        try:
            emoji = await server.create_custom_emoji(name=name, image=emoji_data)
            return True, emoji
        except discord.errors.HTTPException:
            return False, 'Failed to create emoji.'

class Server:
    file = PATH + 'servers.json'
    type = ['item', 'champion']

    @classmethod
    def get_server(cls, type: str) -> int:
        if type not in cls.type:
            raise ValueError(f"Type must be one of {cls.type}")
        try:
            with open(cls.file, 'r') as file:
                data = json.load(file)
            for server in data['data'][type]:
                if server['emoji']['slotsAvailable'] != 0:
                    return server['id']
            return None
        except Exception as error:
            raise RuntimeError(f"Failed to get server ID from {cls.file}") from error

    @classmethod
    def decrease_slot(cls, type: str, server_id: int):
        if type not in cls.type:
            raise ValueError(f"Type must be one of {cls.type}")
        try:
            with open(cls.file, 'r') as file:
                data = json.load(file)
            for server in data['data'][type]:
                if server['id'] == server_id:
                    server['emoji']['slotsAvailable'] -= 1
            with open(cls.file, 'w') as file:
                json.dump(data, file)
        except Exception as error:
            raise RuntimeError(f"Failed to decrease slot for server {server_id}") from error
    

class Item:
    __undef__ = []
    file = PATH + 'items.json'

    @classmethod
    def add_undefined(cls, id: int):
        if id not in cls.__undef__:
            cls.__undef__.append(id)

    @classmethod
    def remove_undefined(cls, id: int):
        if id in cls.__undef__:
            cls.__undef__.remove(id)

    @classmethod
    def get_emoji(cls, id: int) -> str:
        try:
            with open(cls.file, 'r') as file:
                data = json.load(file)
            if str(id) not in data['data']:
                cls.add_undefined(id)
                return data['data'].get('0', None)
            return data['data'].get(str(id), None)
        except Exception as error:
            raise RuntimeError(f"Failed to get emoji for item {id}") from error

    @classmethod
    def set_emoji(cls, id: int, emoji: str):
        try:
            with open(cls.file, 'r') as file:
                data = json.load(file)
            data['data'][str(id)] = emoji

            with open(cls.file, 'w') as file:
                json.dump(data, file)
        except Exception as error:
            raise RuntimeError(f"Failed to set emoji for item {id}") from error

    @classmethod
    async def add_emoji(cls, bot: discord.Client, name: str, url: str):
        server_id = Server.get_server('item')
        if server_id is None:
            raise RuntimeError("No server available")

        success, emoji = await Emoji(bot).create_emoji(server_id, name, url)
        if not success:
            raise RuntimeError(emoji)
        
        cls.set_emoji(name, str(emoji))
        Server.decrease_slot('item', server_id)


class UpdatePlayer:
    file = PATH + 'players.json'
    data = []
    max = 5

    @classmethod
    def save(cls, data: list):
        if not isinstance(data, list):
                raise TypeError("Data must be a list")
        try:
            with open(cls.file, 'w') as file:
                json.dump(data, file)
        except Exception as error:
            raise RuntimeError(f"Failed to save data to {cls.file}") from error

    @classmethod
    def load(cls) -> list:
        try:
            with open(cls.file, 'r') as file:
                cls.data = json.load(file)
        except Exception as error:
            raise RuntimeError(f"Failed to load data from {cls.file}") from error
        else:
            return cls.data

    @classmethod
    def get_summoner_names(cls) -> list:
        try:
            summoner_names = [player.get('summoner').get('name') for player in cls.data]
            return summoner_names
        except Exception as error:
            raise RuntimeError("Failed to get summoner names from") from error

    @classmethod
    def get_region(cls, name: str) -> str:
        try:
            for player in cls.data:
                if player.get('summoner').get('name') == name:
                    return player.get('region')
            return None
        except Exception as error:
            raise RuntimeError(f"Failed to get region for summoner {name}") from error

    @classmethod
    def delete(cls):
        try:
            cls.data.clear()
            cls.save(cls.data)
        except Exception as error:
            raise RuntimeError("Failed to delete data") from error

    @classmethod
    def remove(cls, name: str):
        try:
            player_to_remove = [player for player in cls.data if player.get('summoner').get('name') == name]
            if player_to_remove:
                cls.data.remove(player_to_remove[0])
                cls.save(cls.data)
        except Exception as error:
            raise RuntimeError(f"Failed to remove summoner {name}") from error


class Region(Enum):
    brazil = ['BR', 'BRAZIL']
    europe_north_east = ['EUNE', 'EUROPE NORTH EAST']
    europe_west = ['EUW', 'EUROPE WEST']
    japan = ['JP', 'JAPAN']
    korea = ['KR', 'KOREA']
    latin_america_north = ['LAN', 'LATIN AMERICA NORTH']
    latin_america_south = ['LAS', 'LATIN AMERICA SOUTH']
    north_america = ['NA', 'NORTH AMERICA']
    oceania = ['OCE', 'OCEANIA']
    turkey = ['TR', 'TURKEY']
    russia = ['RU', 'RUSSIA']
    philippines = ['PH', 'PHILIPPINES']
    singapore = ['SG', 'SINGAPORE']
    thailand = ['TH', 'THAILAND']
    taiwan = ['TW', 'TAIWAN']
    vietnam = ['VN', 'VIETNAM']

    @property
    def platform(self) -> 'Platform':
        return getattr(Platform, self.name)

    @staticmethod
    def from_platform(region: str) -> platform:
        try:
            for i in Region:
                if region.upper() in i.value:
                    return i.platform
        except: return None

    @staticmethod
    def get_choices() -> list:
        return [app_commands.Choice(name=f"{i.value[1].capitalize()} ({i.value[0]})", value=i.value[0]) for i in Region]

class Platform(Enum):
    brazil = 'BR1'
    europe_north_east = 'EUN1'
    europe_west = 'EUW1'
    japan = 'JP1'
    korea = 'KR'
    latin_america_north = 'LA1'
    latin_america_south = 'LA2'
    north_america = 'NA1'
    oceania = 'OC1'
    turkey = 'TR1'
    russia = 'RU'
    philippines = 'PH2'
    singapore = 'SG2'
    thailand = 'TH2'
    taiwan = 'TW2'
    vietnam = 'VN2'

    @property
    def region(self) -> 'Region':
        return getattr(Region, self.name)

    @staticmethod
    def from_region(region: str) -> Region:
        try: return region.platform
        except AttributeError: return Platform(region).region


class ddragon:
    url_version = 'http://ddragon.leagueoflegends.com/api/versions.json'
    version = requests.get(url_version).json()[0]

    url_profileIcon = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/'
    url_champion = f'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json'
    url_challenges = f'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/challenges.json'
    url_queues = 'https://static.developer.riotgames.com/docs/lol/queues.json'
    url_runesReforged = f'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json'
    url_summoner = f'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/summoner.json'
    url_item = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/item/'


    @staticmethod
    def get_champion() -> dict:
        return requests.get(ddragon.url_champion).json()

    @staticmethod
    def get_challenges() -> dict:
        return requests.get(ddragon.url_challenges).json()

    @staticmethod
    def get_queues() -> dict:
        return requests.get(ddragon.url_queues).json()
    
    @staticmethod
    def get_runesReforged() -> dict:
        return requests.get(ddragon.url_runesReforged).json()

    @staticmethod
    def get_summoner() -> dict:
        return requests.get(ddragon.url_summoner).json()

    @staticmethod
    def get_item(id: int) -> str:
        return f'{ddragon.url_item}{id}.png'


class Champion():
    @staticmethod
    def from_id(id: int):
        try:
            data = ddragon.get_champion()['data']
            for champion in data:
                if data[champion]['key'] == str(id):
                    name = data[champion]['name']
                    return FIX_NAMES[name] if name in FIX_NAMES else name
        except Exception as error:
            return error

    @staticmethod
    def fix_name(string: str):
        try: return FIX_NAMES[string]
        except KeyError: return string

FIX_NAMES = {
    'AurelionSol': 'Aurelion Sol',
    'Belveth': "Bel'veth",
    'Chogath': "Cho'Gath",
    'DrMundo': 'Dr. Mundo',
    'Fiddlesticks': 'FiddleSticks',
    'JarvanIV': 'Jarvan IV',
    'Kaisa': "Kai'Sa",
    'Khazix': "Kha'Zix",
    'KogMaw': "Kog'Maw",
    'KSante': "K'Sante",
    'Leblanc': 'LeBlanc',
    'LeeSin': 'Lee Sin',
    'MasterYi': 'Master Yi',
    'MissFortune': 'Miss Fortune',
    'MonkeyKing': 'Wukong',
    'Nunu': 'Nunu & Willump',
    'RekSai': "Rek'Sai",
    'TahmKench': 'Tahm Kench',
    'TwistedFate': 'Twisted Fate',
    'Velkoz': "Vel'Koz",
    'XinZhao': 'Xin Zhao',
}

class Challenges():
    @staticmethod
    def from_id(id: int):
        try:
            challengeId = int(id[:-2])
            tierId = CHALLENGES_TIER_IDS[int(id[-1])]
            data = ddragon.get_challenges()
            for challenge in data:
                if challenge['id'] == challengeId:
                    return challenge['thresholds'][tierId]['rewards'][0]['title']
        except: return None

CHALLENGES_TIER_IDS = {
    0:'IRON',
    1:'BRONZE',
    2:'SILVER',
    3:'GOLD',
    4:'PLATINUM',
    5:'DIAMOND',
    6:'MASTER',
    7:'GRANDMASTER',
    8:'CHALLENGER',
}

class Queue():
    map = None
    description = None

    @staticmethod
    def from_id(id: int):
        try:
            data = ddragon.get_queues()
            for queue in data:
                if queue['queueId'] == id:
                    Queue.map = queue['map']
                    Queue.description = Queue.filter(queue['description'])
        except: pass

    @staticmethod
    def filter(string: str) -> str:
        string = string.replace(' games', '')
        string = string.replace('5v5 ', '')
        string = string.replace('3v3 ', '')
        string = string.replace('Solo', 'Solo/Duo')
        string = string.replace('Pick URF', 'Ultra Rapid Fire')
        string = string.replace('Draft Pick', 'Normal (Draft Pick)')
        string = string.replace('Co-op vs. AI', '')
        string = string.replace('Bot', '')
        return string
        

class Rune(Enum):
    arcane_comet = 'Arcane Comet'
    conqueror = 'Conqueror'
    dark_harvest = 'Dark Harvest'
    electrocute = 'Electrocute'
    first_strike = 'First Blood'
    fleet_footwork = 'Fleet Footwork'
    glacial_augment = 'Glacial Augment'
    grasp_of_the_undying = 'Grasp of the Undying'
    guardian = 'Guardian'
    hail_of_blades = 'Hail of Blades'
    lethal_tempo = 'Lethal Tempo'
    phase_rush = 'Phase Rush'
    predator = 'Predator'
    press_the_attack = 'Press the Attack'
    summon_aery = 'Summon Aery'
    unsealed_spellbook = 'Unsealed Spellbook'
    aftershock = 'Aftershock'
    none = 'None'

    @staticmethod
    def from_league(string: str):
        try: return Rune[string.replace(' ','_').lower()]
        except KeyError: return Rune.none

class Summoner(Enum):
    barrier = 'SummonerBarrier'
    boost = 'SummonerBoost'
    dot = 'SummonerDot'
    exhaust = 'SummonerExhaust'
    flash = 'SummonerFlash'
    haste = 'SummonerHaste'
    heal = 'SummonerHeal'
    mana = 'SummonerMana'
    poroRecall = 'SummonerPoroRecall'
    poroThrow = 'SummonerPoroThrow'
    smite = 'SummonerSmite'
    snowURFSnowball_Mark = 'SummonerSnowURFSnowball_Mark'
    snowball = 'SummonerSnowball'
    teleport = 'SummonerTeleport'
    ultBookPlaceholder = 'SummonerUltBookPlaceholder'
    ultBookSmitePlaceholder = 'SummonerUltBookSmitePlaceholder'
    none = 'None'

    @staticmethod
    def from_key(key: int):
        try: return {i: summoner for summoner, i in KEYS.items()}[key]
        except KeyError: return Summoner.none

    @property
    def key(self): 
        return KEYS[self]

KEYS = {
    Summoner.barrier: 21,
    Summoner.boost: 1,
    Summoner.dot: 14,
    Summoner.exhaust: 3,
    Summoner.flash: 4,
    Summoner.haste: 6,
    Summoner.heal: 7,
    Summoner.mana: 13,
    Summoner.poroRecall: 30,
    Summoner.poroThrow: 31,
    Summoner.smite: 11,
    Summoner.snowURFSnowball_Mark: 39,
    Summoner.snowball: 32,
    Summoner.teleport: 12,
    Summoner.ultBookPlaceholder: 54,
    Summoner.ultBookSmitePlaceholder: 55,
    Summoner.none: -1,
}
        
