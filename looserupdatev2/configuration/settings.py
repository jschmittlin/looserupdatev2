from typing import Dict
import discord
import logging
import os


def get_default_config():
    return {
        "globals": { "default_region": "EUW" },
        "riotgames": { "api_key": "RIOT_API_KEY" },
        "discord": {
            "Token": "DISCORD_API_TOKEN",
            "Prefix": "!",
            "Guid_ID": "GUILD_ID",
            "Channel_ID": "CHANNEL_ID",
            "Activities": [
                {
                    "name": "for /help",
                    "type": "playing",
                }
            ],
        },
    }

class Settings(object):
    def __init__(self, settings):
        _default = get_default_config()
        _globals = settings.get("global", _default["globals"])
        self.__default_region = _globals.get(
            "default_region", _default["globals"]["default_region"]
        )

        _riotgames = settings.get("riotgames", _default["riotgames"])
        self.__riot_api_key = os.environ.get(
            _riotgames.get(
                "api_key", _default["riotgames"]["api_key"]
            )
        )

        _discord = settings.get("discord", _default["discord"])
        self.__discord_token = os.environ.get(
            _discord.get(
                "Token", _default["discord"]["Token"]
            )
        )
        self.__discord_prefix = _discord.get(
            "Prefix", _default["discord"]["Prefix"]
        )
        _discord_guild_id = os.environ.get(
            _discord.get(
                "Guid_ID", _default["discord"]["Guid_ID"]
            )
        )
        self.__discord_guild_object = discord.Object(id=_discord_guild_id)
        self.__discord_channel_id = int(os.environ.get(
            _discord.get(
                "Channel_ID", _default["discord"]["Channel_ID"]
            )
        ))
        self.__discord_activities = _discord.get(
            "Activities", _default["discord"]["Activities"]
        )

    @property
    def default_region(self):
        return self.__default_region
    
    @default_region.setter
    def default_region(self, value):
        self.__default_region = value

    @property
    def riot_api_key(self):
        return self.__riot_api_key

    @property
    def discord_token(self):
        return self.__discord_token

    @property
    def discord_prefix(self):
        return self.__discord_prefix

    @property
    def discord_guild_object(self):
        return self.__discord_guild_object

    @property
    def discord_channel_id(self):
        return self.__discord_channel_id
    
    @discord_channel_id.setter
    def discord_channel_id(self, value):
        self.__discord_channel_id = value

    @property
    def discord_activities(self):
        return self.__discord_activities
