import asyncio
import json
from io import BytesIO
from pathlib import Path

import discord
import requests

from core.common import log

DATA_DIR = './LooserUpdateV2/datastores/staticdata/'

class Server:
    file_path = Path(DATA_DIR) / 'servers.json'
    types = ['item', 'champion']

    @classmethod
    def get_server(cls, server_type: str) -> int:
        """Returns the ID of a server with available slots."""
        if server_type not in cls.types:
            raise ValueError(f"Type must be one of {cls.types}")
        
        with open(cls.file_path, 'r') as file:
            json_data = json.load(file)
            
        for server in json_data['data'][server_type]:
            if server['emoji']['slotsAvailable'] != 0:
                return server['id']
            
        return None

    @classmethod
    def decrease_slot(cls, server_type: str, server_id: int) -> None:
        """Decreases the available emoji slots of a server."""
        if server_type not in cls.types:
            raise ValueError(f"Type must be one of {cls.types}")
        
        with open(cls.file_path, 'r') as file:
            json_data = json.load(file)
            
        for server in json_data['data'][server_type]:
            if server['id'] == server_id:
                server['emoji']['slotsAvailable'] -= 1
                
        with open(cls.file_path, 'w') as file:
            json.dump(json_data, file)

class EmojiManager:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def create_emoji(self, server_id: int, name: str, url: str) -> tuple[bool, str]:
        """Creates a new emoji from an image URL."""
        response = requests.get(url)
        if not response.ok:
            return False, 'Failed to get image from URL.'
        
        emoji_data = response.content
        
        server = self.bot.get_guild(server_id)
        if server is None:
            return False, 'Invalid server ID.'
        
        try:
            emoji = await server.create_custom_emoji(name=name, image=emoji_data)
            log(f"Created emoji {name} in server '{server.name}'")
            return True, emoji
        except discord.errors.HTTPException as e:
            return False, f'Failed to create emoji: {e}'
            
class EmojiDataBase:
    _undefined = set()

    @classmethod
    def add_undefined(cls, id: int) -> None:
        """ Adds an item ID to the undefined list. """
        if id not in cls._undefined:
            log(f"Adding {id} to undefined list")
            cls._undefined.add(id)

    @classmethod
    def remove_undefined(cls, id: int) -> None:
        """ Removes an item ID from the undefined list. """
        if id in cls._undefined:
            cls._undefined.remove(id)

    @classmethod
    def get_emoji(cls, id: int) -> str:
        """ Returns the emoji for an item ID. """
        with open(cls.file_path, 'r') as file:
            json_data = json.load(file)
            
        if str(id) not in json_data['data']:
            cls.add_undefined(id)
            return json_data['data'].get('0')
        
        return json_data['data'].get(str(id))

    @classmethod
    def set_emoji(cls, id: int, emoji: str) -> None:
        """ Sets the emoji for an item ID. """
        with open(cls.file_path, 'r') as file:
            json_data = json.load(file)
            
        json_data['data'][str(id)] = emoji
        with open(cls.file_path, 'w') as file:
            json.dump(json_data, file)

    @classmethod
    async def add_emoji(cls, bot: discord.Client, name: str, url: str) -> None:
        """ Adds a new emoji for an item. """
        server_id = Server.get_server(cls.emoji_type)
        if server_id is None:
            raise RuntimeError("No server available")

        success, emoji = await EmojiManager(bot).create_emoji(server_id, name, url)
        if not success:
            raise RuntimeError(emoji)
        
        cls.set_emoji(name, str(emoji))
        Server.decrease_slot(cls.emoji_type, server_id)

class Item(EmojiDataBase):
    file_path = Path(DATA_DIR) / 'items.json'
    emoji_type = 'item'

class Champion(EmojiDataBase):
    file_path = Path(DATA_DIR) / 'champion.json'
    emoji_type = 'champion'