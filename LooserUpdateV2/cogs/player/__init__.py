from ...core.bot import LooserUpdateV2Bot

from .player import Player


async def setup(bot: LooserUpdateV2Bot):
    await bot.add_cog(Player(bot), guild=bot.settings.discord_guild_object)
