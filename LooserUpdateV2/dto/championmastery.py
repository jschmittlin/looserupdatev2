from .common import DtoObject


class ChampionMasteryDto(DtoObject):
    _dict = {                                               # This object contains single Champion Mastery information for player and champion combination.
        "championId": int,                                  # Champion ID for this entry.
        "championLevel": int,                               # Champion level for specified player and champion combination.
        "championPoints": int,                              # Total number of champion points for this player and champion combination - they are used to determine championLevel.
    }

class ChampionMasteryListDto(DtoObject):
    _dict = {
        "championMasteryList": [ChampionMasteryDto._dict], # List of champion mastery information for player.
    }

class ChampionMasteryScoreDto(DtoObject):
    _dict = {
        "score": int,                                       # Player's total champion mastery score, which is the sum of individual champion mastery levels.
    }
