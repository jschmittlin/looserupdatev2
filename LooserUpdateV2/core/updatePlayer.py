from pathlib import Path
import json

DATA_DIR = './LooserUpdateV2/core/staticdata/'

class UpdatePlayer:
    file_path = Path(DATA_DIR) / 'players.json'
    data = []
    max = 5

    @classmethod
    def save(cls, data: list):
        if not isinstance(data, list):
                raise TypeError("Data must be a list")
        try:
            with open(cls.file_path, 'w') as file:
                json.dump(data, file)
        except Exception as error:
            raise RuntimeError(f"Failed to save data to {cls.file_path}") from error

    @classmethod
    def load(cls) -> list:
        try:
            with open(cls.file_path, 'r') as file:
                cls.data = json.load(file)
        except Exception as error:
            raise RuntimeError(f"Failed to load data from {cls.file_path}") from error
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