from .common import DtoObject


class MatchListDto(DtoObject):
    _dict = {
        "match_ids": [str],                                 # List of match IDs.
        "puuid": str,                                       # Encrypted PUUID.
        "queue": str,                                       # The queue type (queue types are documented on the Game Constants page).
        "type": str,                                        # The type of match (Legal values: "ranked", "normal", "tourney", "tutorial").
        "start": int,                                       # The starting index of the list of matches.
        "count": int,                                       # The number of matches to return.
    }

class ObjectiveDto(DtoObject):
    _dict = {
        "kills": int,
    }

class ObjectivesDto(DtoObject):
    _dict = {
        "baron": ObjectiveDto._dict,
        "dragon": ObjectiveDto._dict,
        "inhibitor": ObjectiveDto._dict,
        "riftHerald": ObjectiveDto._dict,
        "tower": ObjectiveDto._dict,
    }

class BanDto(DtoObject):
    _dict = {
        "championId": int,
    }

class TeamDto(DtoObject):
    _dict = {
        "bans": [BanDto._dict],
        "objectives": ObjectivesDto._dict,
        "teamId": int,
        "win": bool,
    }

class PerkStyleSelectionDto(DtoObject):
    _dict = {
        "perk": int,
    }

class PerkStyleDto(DtoObject):
    _dict = {
        "selections": [PerkStyleSelectionDto._dict],
    }

class PerksDto(DtoObject):
    _dict = {
        "styles": [PerkStyleDto._dict],
    }

class ParticipantDto(DtoObject):
    _dict = {
        "assists": int,
        "champLevel": int,
        "championId": int,
        "deaths": int,
        "goldEarned": int,
        "item0": int,
        "item1": int,
        "item2": int,
        "item3": int,
        "item4": int,
        "item5": int,
        "item6": int,
        "kills": int,
        "neutralMinionsKilled": int,
        "perks": PerksDto._dict,
        "playerAugment1": int,
        "playerAugment2": int,
        "playerAugment3": int,
        "playerAugment4": int,
        "playerSubteamId": int,
        "puuid": str,
        "role": str,
        "subteamPlacement": int,
        "summoner1Id": int,
        "summoner2Id": int,
        "summonerName": str,
        "teamId": int,
        "teamPosition": str,                                # The teamPosition is the best guess for which position the player actually played if we add the constraint that each team must have one top player, one jungler, one middle, etc.
        "totalAllyJungleMinionsKilled": int,
        "totalEnemyJungleMinionsKilled": int,
        "totalMinionsKilled": int,
        "win": bool,
    }

class InfoDto(DtoObject):
    _dict = {
        "gameDuration": int,                                # The game legnth in milliseconds calculated from gameEndTimestamp - gameStartTimestamp.
        "gameEndTimestamp": int,                            # Unix timestamp for when match ends on the game server.
        "gameMode": str,                                    # Refer to the Game Constants documentation.
        "participants": [ParticipantDto._dict],
        "queueId": int,                                     # Refer to the Game Constants documentation.
        "teams": [TeamDto._dict],
    }

class MatchDto(DtoObject):
    _dict = {
        "info": InfoDto._dict,                              # Match info.
    }
