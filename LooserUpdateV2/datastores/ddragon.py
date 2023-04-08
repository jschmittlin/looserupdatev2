import requests

class DDragon:
    """ A class for getting data from the League of Legends DDragon API. """
    
    def __init__(self):
        self.version = requests.get('http://ddragon.leagueoflegends.com/api/versions.json').json()[0]
        self.url = {
            'data': {
                'champion': f'http://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion.json',
                'challenges': f'https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/challenges.json',
                'queues': 'https://static.developer.riotgames.com/docs/lol/queues.json',
                'runesReforged': f'http://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/runesReforged.json',
                'summoner': f'http://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/summoner.json'
            },
            'img': {
                'profileIcon': f'http://ddragon.leagueoflegends.com/cdn/{self.version}/img/profileicon/',
                'item': f'http://ddragon.leagueoflegends.com/cdn/{self.version}/img/item/',
                'champion': f'http://ddragon.leagueoflegends.com/cdn/{self.version}/img/champion/'
            }
        }

    @classmethod
    def get_champion(cls) -> dict:
        """ Returns a dictionary of all champions. """
        response = requests.get(cls().url['data']['champion'])
        response.raise_for_status()
        return response.json()['data']

    @classmethod
    def get_challenges(cls) -> dict:
        """ Returns a dictionary of all challenges. """
        response = requests.get(cls().url['data']['challenges'])
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_queues(cls) -> dict:
        """ Returns a dictionary of all queues. """
        response = requests.get(cls().url['data']['queues'])
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_runes_reforged(cls) -> dict:
        """ Returns a dictionary of all runes. """
        response = requests.get(cls().url['data']['runesReforged'])
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_summoner(cls) -> dict:
        """ Returns a dictionary of all summoner spells. """
        response = requests.get(cls().url['data']['summoner'])
        response.raise_for_status()
        return response.json()
    
    @classmethod
    def get_profile_icon(cls, id: int) -> str:
        """ Returns the URL of the profile icon image. """
        return f"{cls().url['img']['profileIcon']}{id}.png"

    @classmethod
    def get_item(cls, id: int) -> str:
        """ Returns the URL of the item image. """
        return f"{cls().url['img']['item']}{id}.png"

    @classmethod
    def get_champion_square_assets(cls, name: str) -> str:
        """ Returns the URL of the champion square assets. """
        return f"{cls().url['img']['champion']}{name}.png"