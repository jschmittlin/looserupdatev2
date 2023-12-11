from typing import Optional, Union
import os
import json
import requests
import discord
import asyncio

import logging

LOGGER = logging.getLogger("looserupdatev2.core.emoji")


class Server:
    _file = "servers.json"
    _type = "server"
    _data_types = ["item", "champion", "summonerspell", "rune", "augment"]

    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.load_json(self._file)

    def load_json(self, file: Optional[str] = None):
        if file is None:
            file = self._file
        file_name = os.path.join(os.path.dirname(__file__), "../../datastores/data", file)
        with open(file_name, "r") as json_file:
            json_data = json.load(json_file)
        self._data = json_data["data"]

    def to_json(self, file: Optional[str] = None, data: Optional[dict] = None):
        if file is None:
            file = self._file
        if data is None:
            data = self._data
        file_name = os.path.join(os.path.dirname(__file__), "../../datastores/data", file)
        with open(file_name, "w") as json_file:
            json.dump({"type": self._type, "data": data}, json_file)

    def _get_guild(self, id: int) -> discord.Guild:
        guild = self.bot.get_guild(id)
        if guild is None:
            raise ValueError(f"Invalid server ID: {id}")
        return guild

    def _get_server_available(self, type: str) -> Optional[int]:
        if type not in self._data_types:
            raise ValueError(f"Type must be one of {self._data_types}")

        if type not in self._data:
            raise ValueError(f"Type {type} not found in data")

        for server in self._data[type]:
            if server["emoji"]["slotsAvailable"] > 0:
                return server["id"]
        return None

    async def _update_available_slots(self, guild: discord.Guild) -> None:
        discord_free_slots = 50

        try:
            emojis = await guild.fetch_emojis()
        except discord.HTTPException as error:
            raise RuntimeError(f"Unable to fetch emojis from {guild.name} ({guild.id}): {error}")

        nb_emojis = len(emojis)

        for _type, servers in self._data.items():
            for server in servers:
                if server["id"] == guild.id:
                    server["emoji"]["slotsAvailable"] = discord_free_slots - nb_emojis
                    LOGGER.debug(f"Available slots for {guild.name} ({guild.id}): {server['emoji']['slotsAvailable']}")
                    return

    async def create_emoji(self, type: str, name: str, url: str) -> Optional[discord.Emoji]:
        guild_id = self._get_server_available(type)
        if guild_id is None:
            return None

        guild = self._get_guild(id=guild_id)

        try:
            image = requests.get(url).content
        except requests.exceptions.RequestException as error:
            LOGGER.error(f"Unable to retrieve image from {url}: {error}")
            return None

        try:
            emoji = await guild.create_custom_emoji(name=name, image=image)
            LOGGER.info(f"Created emoji '{emoji}' on {type} {guild.name}")
            await self._update_available_slots(guild=guild)
            return emoji
        except (requests.exceptions.RequestException, discord.HTTPException) as error:
            LOGGER.error(f"Unable to create emoji '{name}' on {type} {guild.name}: {error}")
            return None

    async def _delete_emojis_server(self, id: int) -> None:
        guild = self._get_guild(id=id)
        count = 0
        LOGGER.info(f"Deleting all emojis on {guild.name} ({guild.id})...")
        for emoji in guild.emojis:
            await guild.delete_emoji(emoji)
            count += 1
            LOGGER.info(f"Emojis deleted - '{emoji}'")
            await asyncio.sleep(1)
        await self._update_available_slots(guild=guild)
        LOGGER.info(f"Deleted all emojis on {guild.name} ({guild.id}): '{count}' emojis deleted")
    
    async def delete_all_emojis(self, type: str) -> None:
        if type not in self._data_types:
            raise ValueError(f"Type must be one of {self._data_types}")

        LOGGER.info(f"Deleting all emojis for type {type}...")
        for servers in self._data[type]:
            await self._delete_emojis_server(id=servers["id"])
            await asyncio.sleep(1)
        self.to_json(file=self._file, data=self._data)
        LOGGER.info(f"Deleted all emojis for type {type}")



class EmojiObject(object):
    _undefined = set()

    def __init__(self):
        if hasattr(self, "_file"):
            self.load_json(self._file)

    def load_json(self, file: Optional[str] = None):
        if file is None:
            file = self._file
        file_name = os.path.join(os.path.dirname(__file__), "../../datastores/data", file)
        with open(file_name, "r") as json_file:
            json_data = json.load(json_file)
        self._data = json_data["data"]

    def to_json(self, file: Optional[str] = None, data: Optional[dict] = None):
        if file is None:
            file = self._file
        if data is None:
            data = self._data
        file_name = os.path.join(os.path.dirname(__file__), "../../datastores/data", file)
        with open(file_name, "w") as json_file:
            json.dump({"type": self._data_type, "data": data}, json_file)

    def _add_undefined(self, id: Union[int, str], type: str) -> None:
        if (id, type) not in self.__class__._undefined:
            self.__class__._undefined.add((id, type))

    def _remove_undefined(self, id: Union[int, str], type: str) -> None:
        if (id, type) in self.__class__._undefined:
            self.__class__._undefined.remove((id, type))
        else:
            LOGGER.warning(f"{self._data_type} '{id}' - not found in undefined list")

    def get_emoji(self, id: int) -> str:
        if str(id) not in self._data:
            if not id is None and not id == 0 and not str(id) == "0":
                LOGGER.warning(f"{self._data_type} '{id}' - not found in data")
                self._add_undefined(id=id, type=self._data_type)
            return self._data["__undefined__"]
        return self._data.get(str(id), "__undefined__")

    async def add_emoji(self, server: Server, name: str, url: str) -> None:
        emoji = await server.create_emoji(self._data_type, name, url)
        if emoji is None:
            return
        self._data[str(emoji.name)] = str(emoji)
        self.to_json()
        self._remove_undefined(id=name, type=self._data_type)

    async def delete_all_emojis(self, server: Server) -> None:
        await server.delete_all_emojis(self._data_type)
        self._data = self._data_default["data"]
        self.to_json()
