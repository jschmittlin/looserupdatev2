import logging
from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules

from discord.ext import commands
from discord.ext.commands import AutoShardedBot

from .help import Help
from .player import Player
from .profile import Profile
from .region import Region

LOGGER = logging.getLogger("looserupdatev2.cogs")

__all__ = [
    "Help",
    "Player",
    "Profile",
    "Region",   
]


async def load_all_cogs(bot: AutoShardedBot) -> AutoShardedBot:
    package_dir = Path(__file__).resolve().parent.absolute()
    for info in iter_modules([str(package_dir)]):
        module = import_module(f"{__name__}.{info.name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (
                isclass(attribute)
                and issubclass(attribute, commands.Cog)
                and attribute.__name__ in __all__
            ):
                if module.__name__ in bot.extensions:
                    LOGGER.info(f"reloading extension {module.__name__}")
                    await bot.reload_extension(module.__name__)
                else:
                    LOGGER.info(f"loading extension {module.__name__}")
                    await bot.load_extension(module.__name__)
    return bot
