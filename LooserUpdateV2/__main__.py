import discord

from . import configuration
from .core import LooserUpdateV2Bot


async def main():
    discord.utils.setup_logging()
    async with LooserUpdateV2Bot() as bot:
        await bot.start(configuration.settings.discord_token)
