from ...core.bot import LooserUpdateV2Bot

from .profile import Profile


async def setup(bot: LooserUpdateV2Bot):
    await bot.add_cog(Profile(bot), guild=bot.settings.discord_guild_object)
