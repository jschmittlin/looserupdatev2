class Color:
    default=0x1e1f22    # black
    error=0xf0e6d2      # white
    victory=0x0f93ad    # blue
    defeat=0xa42f3f     # red

    ansi_reset="[0;0m"
    ansi_gray="[0;30m"
    ansi_red="[0;31m"
    ansi_green="[0;32m"
    ansi_yellow="[0;33m"
    ansi_blue="[0;34m"
    ansi_pink="[0;35m"
    ansi_cyan="[0;36m"
    ansi_white="[0;37m"
    ansi_bold = "[1m"

    @classmethod
    def discord_preset_error(cls, error: str) -> str:
        return (
            f"```ansi\n"
            f"{cls.ansi_red}{cls.ansi_bold}"
            f"{error}"
            f"{cls.ansi_reset}"
            f"```"
        )

    @classmethod
    def discord_preset_region(cls, region: object) -> str:
        return (
            f"```ansi\n"
            f"{cls.ansi_white}{cls.ansi_bold}"
            f"{region.name.replace('_', ' ').title()} "
            f"{cls.ansi_gray}"
            f"#{region.value}"
            f"{cls.ansi_reset}"
            f"```"
        )

    @classmethod
    def discord_preset_player(cls, gameName: str, tagLine: str) -> str:
        return (
            f"```ansi\n"
            f"{cls.ansi_white}{cls.ansi_bold}"
            f"{gameName} "
            f"{cls.ansi_gray}"
            f"#{tagLine}"
            f"{cls.ansi_reset}"
            f"```"
        )
