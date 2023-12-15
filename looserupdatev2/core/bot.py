from typing import Optional
import logging
import random
import asyncio

import discord
from discord.ext import tasks
from discord.ext.commands import AutoShardedBot

from .. import configuration

LOGGER = logging.getLogger("looserupdatev2.bot")


class LooserUpdateV2Bot(AutoShardedBot):
    to_update = True
    
    def __init__(self):
        self.settings = configuration.settings
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=configuration.settings.discord_prefix,
            intents=intents,
        )

    async def on_ready(self):
        LOGGER.info(f"logged in as {self.user}")

    async def setup_hook(self):
        # load all cog extensions and application commands
        from ..configuration.load import load_extensions

        await load_extensions(self, do_sync=False)

        # start all tasks
        self.change_activity_loop.start()
        self.update_ddragon_cache_loop.start()
        self.add_undefined_emojis_loop.start()
        self.update_players_loop.start()

    @tasks.loop(minutes=20)
    async def change_activity_loop(self) -> None:
        activity = random.choice(self.settings.discord_activities)
        await self.change_presence(activity=discord.Activity(type=getattr(discord.ActivityType, activity["type"]), name=activity["name"]))

    @tasks.loop(hours=24)
    async def update_ddragon_cache_loop(self) -> None:
        from .common import (
            ddragon,    
            get_latest_version,
            get_data_dragon,
            get_data_cdragon,
        )

        files = [
            "challenges.json",
            "champion.json",
            "item.json",
            "summoner.json",
            "runesReforged.json",
            "spellbuffs.json",
        ]

        ddragon["version"] = get_latest_version()
        for file in files:
            if file == "spellbuffs.json":
                ddragon["cache"][file] = get_data_cdragon(file=file)
            else:
                ddragon["cache"][file] = get_data_dragon(file=file)
            await asyncio.sleep(1) 

    @tasks.loop(minutes=1)
    async def add_undefined_emojis_loop(self) -> None:
        from .staticdata.common import Server, EmojiObject

        undefined = EmojiObject()._undefined.copy()
        if len(undefined) == 0:
            return

        LOGGER.info(f"Adding {len(undefined)} undefined emojis...")
        server = Server(bot=self)
        for id, type in undefined:
            if type == "champion":
                from .staticdata.champion import Champion
                champion = Champion(id=id)
                await champion.emoji.add_emoji(
                    server=server, name=champion.id, url=champion.url
                )
                pass
            if type == "item":
                from .staticdata.item import Item
                item = Item(id=id, image=f"{id}.png")
                await item.emoji.add_emoji(
                    server=server, name=item.id, url=item.url
                )
                pass
            if type == "summonerspell":
                from .staticdata.summonerspell import SummonerSpell
                summonerspell = SummonerSpell(id=id)
                await summonerspell.emoji.add_emoji(
                    server=server, name=summonerspell.id, url=summonerspell.url
                )
                pass
            if type == "rune":
                from .staticdata.rune import Rune
                rune = Rune(id=id)
                await rune.emoji.add_emoji(
                    server=server, name=rune.id, url=rune.url
                )
                pass
            if type == "augment":
                from .staticdata.augment import Augment
                augment = Augment(id=id)
                await augment.emoji.add_emoji(
                    server=server, name=augment.id, url=augment.url
                )
                pass

        server.to_json()
        LOGGER.info(f"Done adding {len(undefined)} undefined emojis")
    
    @tasks.loop(minutes=2)
    async def update_players_loop(self) -> None:
        from .player import PlayerList
        from .embed import Embed
        from .view import UpdatePlayerView

        if not self.to_update:
            return

        players = PlayerList()
        for player in players:
            if player.update_rank():
                LOGGER.info(f"Updated {player.name}'s solo rank")

                channel = self.get_channel(self.settings.discord_channel_id)
                if channel is None:
                    LOGGER.error(f"Unable to find channel with id {self.settings.discord_channel_id}")
                    LOGGER.warning(f"Channel is not set, update player will not be sent")
                    self.to_update = False
                    return

                embed = Embed.player_update(player=player)
                view = UpdatePlayerView(player=player)
                await channel.send(embed=embed, view=view)
            await asyncio.sleep(1) 

        players.to_json()

    @change_activity_loop.before_loop
    async def before_change_activity_loop(self):
        await self.wait_until_ready()

    @update_ddragon_cache_loop.before_loop
    async def before_update_ddragon_cache_loop(self):
        await self.wait_until_ready()

    @add_undefined_emojis_loop.before_loop
    async def before_add_undefined_emojis_loop(self):
        await self.wait_until_ready()

    @update_players_loop.before_loop
    async def before_update_players_loop(self):
        await self.wait_until_ready()
