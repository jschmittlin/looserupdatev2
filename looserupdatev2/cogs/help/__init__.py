from ...core.bot import LooserUpdateV2Bot

from .help import Help


async def setup(bot: LooserUpdateV2Bot):
    await bot.add_cog(Help(bot), guild=bot.settings.discord_guild_object)
