from .common import DtoObject


class LeagueEntryDto(DtoObject):
    _dict = {
        "queueType": str,                                   # The league's queue type.
        "tier": str,                                        # The league's tier.
        "rank": str,                                        # The player's division within a tier.
        "leaguePoints": int,                                # League points.
        "wins": int,                                        # Winning team on Summoners Rift.
        "losses": int,                                      # Losing team on Summoners Rift.
    }

class LeagueEntriesDto(DtoObject):
    _dict = {
        "entries": [LeagueEntryDto._dict],                  # The requested league entries.
    }
