from ...core.bot import LooserUpdateV2Bot

from .region import Region


async def setup(bot: LooserUpdateV2Bot):
    await bot.add_cog(Region(bot), guild=bot.settings.discord_guild_object)
