from typing import Dict
from discord.ext.commands import AutoShardedBot
from dotenv import load_dotenv
import logging
import asyncio
import os

try:
    import ujson as json
except ImportError:
    import json

LOGGER = logging.getLogger("looserupdatev2.load")
load_dotenv()


def load_config(filename=None) -> Dict:
    head, tail = os.path.split(__file__)

    if filename is not None:
        if not os.path.exists(filename):
            filename = os.path.normpath(os.path.join(head, filename))
            if not os.path.exists(filename):
                raise FileNotFoundError(f"config file '{filename}' not found.")
        config = json.loads(open(filename).read())
    else:
        config = {}
    return config

async def load_extensions(bot: AutoShardedBot, do_sync: bool = False) -> None:
    from ..cogs import load_all_cogs

    guild = bot.settings.discord_guild_object

    if do_sync:
        if guild:
            LOGGER.info(f"syncing commands to debug guild {guild.id}")
        else:
            LOGGER.info("syncing commands globally")

        LOGGER.info("clearing commands...")
        bot.tree.clear_commands(guild=guild)
        await bot.tree.sync(guild=guild)

        LOGGER.info("waiting to avoid rate limits...")
        await asyncio.sleep(1)

    LOGGER.info("loading cogs...")
    await load_all_cogs(bot)
    commands = [c.name for c in bot.tree.get_commands(guild=guild)]
    LOGGER.info("registered commands: " + ", ".join(commands))

    if do_sync:
        LOGGER.info("syncing commands...")
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
