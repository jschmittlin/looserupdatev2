from .common import DtoObject


class PlayerClientPreferencesDto(DtoObject):
    _dict = {
        "title": str,                                       # Title of the player.
        "challengeIds": [int],                              # List of challenge IDs.
    }

class ChallengePointsDto(DtoObject):
    _dict = {
        "level": str,                                       # Level of the challenge.
        "current": int,                                     # Current progress of the challenge.
        "max": int,                                         # Maximum progress of the challenge.
    }

class CategoryPointsDto(DtoObject):
    _dict = {
        "EXPERTISE": ChallengePointsDto._dict,              # Expertise category.
        "VETERANCY": ChallengePointsDto._dict,              # Veterancy category.
        "COLLECTION": ChallengePointsDto._dict,             # Collection category.
        "TEAMWORK": ChallengePointsDto._dict,               # Teamwork category.
        "IMAGINATION": ChallengePointsDto._dict,            # Imagination category.
    }

class PlayerInfoDto(DtoObject):
    _dict = {
        "totalPoints": ChallengePointsDto._dict,            # Total points.
        "categoryPoints": CategoryPointsDto._dict,          # Category points.
        "preferences": PlayerClientPreferencesDto._dict,    # Player preferences.
    }
