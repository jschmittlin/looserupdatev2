from .common import DtoObject


class SummonerDto(DtoObject):       
    _dict = {
        "profileIconId": int,                               # ID of the summoner icon associated with the summoner.
        "name": str,                                        # Summoner name.
        "id": str,                                          # Encrypted summoner ID. Max length 63 characters.
        "puuid": str,                                       # Encrypted PUUID. Exact length of 78 characters.
        "summonerLevel": int,                               # Summoner level associated with the summoner.
    }
