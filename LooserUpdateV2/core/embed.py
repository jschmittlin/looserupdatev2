from typing import Union, List
import discord

from .summoner import Summoner
from .match import Match
from .player import Player, PlayerList
from ..data import Region, Queue, Tier, Lane

from ..resources import Icon, Color 
from ..resources.emoji import blank, Mastery, Match

# TODO: change for blitz.gg link and add link for match
def opgg(name: str, region: str) -> str:
    return f"https://www.op.gg/summoners/{region.lower()}/{name.replace(' ', '%20')}"

def get_winrate(wins: int, losses: int) -> Union[int, str]:
    try:
        return round(wins / (wins + losses) * 100)
    except ZeroDivisionError:
        return "?"

def get_kda(kills: int, deaths: int, assists: int) -> Union[int, str]:
    try:
        return round((kills + assists) / deaths, 2)
    except ZeroDivisionError:
        return round((kills + assists) / 1, 2)

def get_kp(kills: int, assists: int, team_kills: int) -> Union[int, str]:
    try:
        return round((kills + assists) / team_kills * 100)
    except ZeroDivisionError:
        return "?"


class Embed:
    @staticmethod
    def error(type: str, error: str) -> discord.Embed:
        return discord.Embed(
            description=(
                f"{Color.discord_preset_error(error=error)}\n"
                "**Sorry, the developer made a mistake. Please send a bug report.\n\n"
                "Try '/help' for more information.**"
            ),
            color=Color.error,
        ).set_author(
            name=f"{type.upper()} ERROR", icon_url=Icon.ux_x,
        ).set_thumbnail(
            url=Icon.random_poro(happy=False),
        )

    @staticmethod
    def help(commands: List["Command"]) -> discord.Embed:
        embed = discord.Embed(
            description="### Commands List", color=Color.default,
        ).set_author(
            name="HELP", icon_url=Icon.ux_search,
        ).set_thumbnail(
            url=Icon.random_poro(happy=True),
        )
        for c in commands:
            embed.add_field(
                name=f"/{c.name}", value=f"```{c.description}```", inline=False,
            )
        return embed

    @staticmethod
    def region_edit(region: Union[Region, str]) -> discord.Embed:
        if not isinstance(region, Region):
            region = Region(region)
        return discord.Embed(
            description=(
                f"{Color.discord_preset_region(region=region)}\n"
                f"**Selected as default region.**{blank * 5}"
            ),
            color=Color.default,
        ).set_author(
            name="EDIT REGION", icon_url=Icon.ux_edit,
        ).set_thumbnail(
            url=region.icon,
        )

    @staticmethod
    def player_add(player: Player) -> discord.Embed:
        return discord.Embed(
            description=(
                f"{Color.discord_preset_player(gameName=player.name, tagLine=player.region.value)}\n"
                f"**Add to the update list.**{blank * 5}"
            ),
            color=Color.default,
        ).set_author(
            name="PLAYER ADD", icon_url=Icon.ux_add,
        ).set_thumbnail(
            url=player.profile_icon.url,
        )

    @staticmethod
    def player_remove(player: Player) -> discord.Embed:
        return discord.Embed(
            description=(
                f"{Color.discord_preset_player(gameName=player.name, tagLine=player.region.value)}\n"
                f"**Remove to the update list.**{blank * 5}"
            ),
            color=Color.default,
        ).set_author(
            name="PLAYER REMOVE", icon_url=Icon.ux_remove,
        ).set_thumbnail(
            url=player.profile_icon.url,
        )

    @staticmethod
    def player_error(error: str) -> discord.Embed:
        return discord.Embed(
            description=(
                f"{Color.discord_preset_error(error=error)}\n"
                f"**Try '/help' for more information.**{blank * 4}"
            ),
            color=Color.error,
        ).set_author(
            name="PLAYER COMMAND ERROR", icon_url=Icon.ux_x,
        ).set_thumbnail(
            url=Icon.random_poro(happy=False),
        )

    @staticmethod
    def player_list(players: PlayerList) -> discord.Embed:
        embed = discord.Embed(
            color=Color.default,
        ).set_author(
            name="UPDATE PLAYER LIST", icon_url=Icon.ux_menu,
        )
        players_value = ''.join([
            f"```ansi\n"
            f"{Color.ansi_white}{Color.ansi_bold}{player.name} {Color.ansi_gray}#{player.region.value}\n"
            f"{f'{player.tier.color}{player.tier} {player.division.value} {Color.ansi_reset}(Solo/Duo)' if player.tier else f'{Tier.unranked.color}{Tier.unranked}'}"
            f"```"
            for player in players
        ]) or "``` ```"
        embed.add_field(
            name=f"**PLAYER MANAGE (MAX PLAYER {players._max_size})**{blank * 6}", value=players_value, inline=False,
        )
        return embed

    @staticmethod
    def player_update(player: Player) -> discord.Embed:
        match = player.match
        info = match.info
        match_player = next((p for p in info.participants if p.puuid == player.puuid), info.participants[0])
        space_max = 61
        rank_color = player.tier.color if player.tier else Tier.unranked.color
        win_color = Color.ansi_blue if match_player.win else Color.ansi_red
        rank = f"{player.tier} {player.division.value}" if player.tier else f"{Tier.unranked}"
        lp = f"{player.league_points} LP"
        winrate = f"{get_winrate(player.wins, player.losses)}% Win Rate"
        win_loss = f"{player.wins}W - {player.losses}L"
        split = " • "
        nb_space_1 = space_max - (len(rank) + len(lp) + len(player.description) + len(split))
        nb_space_2 = space_max - (len(win_loss) + len(winrate))
        embed = discord.Embed(
            description=(
                f"```ansi\n"
                f"{rank_color}{rank}{' ' * nb_space_1}{win_color}{player.description}{Color.ansi_gray}{split}{Color.ansi_reset}{lp}"
                f"\n{Color.ansi_gray}"
                f"{winrate}{' ' * nb_space_2}{win_loss}"
                f"```"
                f"{blank}"
            ),
            color=Color.victory if match_player.win else Color.defeat,
        ).set_author(
            name=f"{player.name} \u200b #{player.region.value}",
            icon_url=player.profile_icon.url,
            url=opgg(player.name, player.region.value),
        )
        Embed.match_mini(embed=embed, puuid=player.puuid, match=match)
        
        return embed

    @staticmethod
    def error_summoner(error: str) -> discord.Embed:
        return discord.Embed(
            description=(
                f"{Color.discord_preset_error(error=f'{error} - summoner not found')}\n"
                "**Something went horribly wrong executing that command, please try again in a bit. "
                "If this error keeps happening, please send a bug report.\n\n"
                "Try '/help' for more information.**"
            ),
            color=Color.error,
        ).set_author(
            name="SUMMONER COMMAND ERROR", icon_url=Icon.ux_x,
        ).set_image(
            url=Icon.bot_error
        )

    @staticmethod
    def profile_overview(summoner: Summoner) -> discord.Embed:
        champion_masteries = summoner.champion_masteries
        league = summoner.league_entries
        challenges = summoner.challenges

        title = f'*{challenges.preferences.title.title}*\n' if challenges.preferences.title.title else ''

        embed = discord.Embed(
            description=(
                f"{Mastery.mastery} **{champion_masteries.score}**{blank * 16}Lvl.{summoner.level}\n"
                f"{title}"
                f"```ansi\n{Color.ansi_gray}—————————————————————————————————————————————————```"
            ),
            color=Color.default,
        ).set_author(
            name=f"{summoner.name} \u200b #{summoner.region.value}",
            icon_url=summoner.profile_icon.url,
            url=opgg(summoner.name, summoner.region.value),
        ).set_thumbnail(
            url=summoner.profile_icon.url,
        ).set_footer(
            text=summoner.region, icon_url=summoner.region.icon,
        )
        try:
            solo = league.solo
            embed.add_field(
                name="**SOLO/DUO**",
                value=(
                    f"{solo.tier.emoji} `{solo.tier} {solo.division.value}`{blank * 3}{solo.league_points} LP\n"
                    f"{get_winrate(solo.wins, solo.losses)}% Win Rate{blank * 3}{solo.wins}W - {solo.losses}L\n"
                    f"{blank * 10}"
                ),
                inline=True,
            )
        except ValueError:
            embed.add_field(
                name="**SOLO/DUO**",
                value=f"{Tier.unranked.emoji} `{Tier.unranked}`\n{blank * 10}",
                inline=True,
            )
        try:
            flex = league.flex
            embed.add_field(
                name="**FLEX 5V5**",
                value=(
                    f"{flex.tier.emoji} `{flex.tier} {flex.division.value}`{blank * 3}{flex.league_points} LP\n"
                    f"{get_winrate(flex.wins, flex.losses)}% Win Rate{blank * 3}{flex.wins}W {flex.losses}L\n"
                    f"{blank * 10}"
                ),
                inline=True,
            )
        except ValueError:
            embed.add_field(
                name="**FLEX 5V5**",
                value=f"{Tier.unranked.emoji} `{Tier.unranked}`\n{blank * 10}",
                inline=True,
            )
        masteries_fields = []
        for mastery in champion_masteries.champion_mastery_list:
            length_caracter = 15 - len(mastery.champion.name)
            space = " \u200b  \u200b " * length_caracter
            s = f"{mastery.champion.get_emoji} `{mastery.champion.name}`{space}{Mastery.mastery} {mastery.points:,} pts"
            masteries_fields.append(s)
        embed.add_field(
            name="**HIGHEST CHAMPION MASTERY**",
            value="\n".join(masteries_fields) + blank,
            inline=False,
        )
        return embed

    @staticmethod
    def match_mini(embed: discord.Embed, puuid: str, match: Match) -> None:
        info = match.info
        queue = info.queue

        player = next((p for p in info.participants if p.puuid == puuid), info.participants[0])

        map_emoji = queue.emoji_victory if player.win else queue.emoji_defeat
        items_emoji = " ".join(item.get_emoji for item in player.items)
        position_emoji = f"{player.position.emoji_hover} {player.position}"
        kda_data = str(get_kda(player.kills, player.deaths, player.assists)).replace('.', ',')
        
        field_2_blank = ""
        if player.position == Lane.top:
            field_2_blank = blank * 1
        if player.position == Lane.jungle:
            field_2_blank = " \u200b "
        if player.position == Lane.middle:
            field_2_blank = blank * 1 + " \u200b \u200b \u200b"
        if player.position == Lane.bottom:
            field_2_blank = blank * 1
        if player.position == Lane.utility:
            field_2_blank = ""
        if player.position == Lane.unselected:
            field_2_blank = blank * 1

        if queue == Queue.aram:
            field_2_blank = blank * 5 + " \u200b "
        if queue == Queue.normal_draft_five:
            field_2_blank = ""
        if queue == Queue.ranked_solo_five:
            field_2_blank = ""
        if queue == Queue.ranked_flex_five:
            field_2_blank += " \u200b \u200b \u200b \u200b"

        embed.add_field(
            name=f"**{map_emoji} \u200b \u200b {Match.victory if player.win else Match.defeat}**{blank}",
            value=(
                f"{player.champion.get_emoji}"
                f"{blank}"
                f"{player.spell_d.get_emoji} {player.spell_f.get_emoji}\n"
                f"**{player.kills} / {player.deaths} / {player.assists}**"
                
            ),
            inline=True,
        )
        embed.add_field(
            name=f"**{field_2_blank}{position_emoji} \u200b \u200b • \u200b \u200b {queue.description}**",
            value=(
                f"{player.runes[0].get_emoji}"
                f"{blank}{items_emoji}\n"
                f"{Match.kda} **{kda_data}**"
                f"{blank}"
                f"{Match.minions} **{player.creep_score:,}**"
                f"{blank}"
                f"{Match.gold} **{player.gold:,}**"
            ),
            inline=True,
        )
        embed.add_field(
            name=f"**• \u200b \u200b {queue.map}**",
            value=(
                f"**{info.duration} \u200b \u200b • \u200b \u200b <t:{info.end_timestamp}:R>**\n"
            ),
            inline=True,
        )

    @staticmethod
    def match_team(embed: discord.Embed, team_id: int, team: "Team", participants: List["Participant"]) -> None:
        objectives = team.objectives

        field_1_value = field_2_value = field_3_value = ""
        total_kills = total_deaths = total_assists = total_gold = 0

        for participant in participants:
            total_kills += participant.kills
            total_deaths += participant.deaths
            total_assists += participant.assists
            total_gold += participant.gold

            name = participant.name
            truncated_name = name[:12] + "..." if len(name) > 15 else name
            champion_emoji = participant.champion.get_emoji
            champion_level = f"`{participant.level}`" if participant.level > 9 else f"\u200b `{participant.level}` \u200b "
            kda = f"{participant.kills} / {participant.deaths} / {participant.assists}"
            items_emoji = " ".join(item.get_emoji for item in participant.items)
            main_rune_emoji = participant.runes[0].get_emoji
            gold = participant.gold

            kda_blank = " "
            if participant.kills < 10:
                kda_blank += "\u200b \u200b "
            if participant.deaths < 10:
                kda_blank += "\u200b \u200b "
            if participant.assists < 10:
                kda_blank += "\u200b \u200b "

            field_1_value += f"{main_rune_emoji} {champion_emoji} {champion_level} `{truncated_name}`\n"
            field_2_value += f"{items_emoji}\n"
            field_3_value += f"`{kda}`{kda_blank}`{gold} GOLD`\n"

        embed.add_field(
            name=f"{Match.team1 if team_id == 100 else Match.team2}{blank * 2}{total_kills} / {total_deaths} / {total_assists}",
            value=field_1_value,
            inline=True,
        )
        embed.add_field(
            name=(
                f" \u200b {blank} \u200b {Match.baron} {objectives.baron.kills} \u200b "
                f"{Match.herald} {objectives.rift_herald.kills} \u200b "
                f"{Match.dragon} {objectives.dragon.kills}"
            ),
            value=field_2_value,
            inline=True,
        )
        embed.add_field(
            name=(
                f"{Match.tower}{objectives.tower.kills} \u200b "
                f"{Match.inhibitor} {objectives.inhibitor.kills}{blank}{Match.gold} {total_gold}"
            ),
            value=field_3_value,
            inline=True,
        )

    @staticmethod
    def profile_match_history(summoner: Summoner) -> discord.Embed:
        match_history = summoner.match_history
        embed = discord.Embed(
            description=(
                f"### RECENT GAMES (LAST 5 PLAYED)\n"
                f"``` ```"
                #f"```ansi\n{Color.ansi_gray}—————————————————————————————————————————————————————————————```"
            ),
            color=Color.default,
        )
        Embed.match_mini(embed=embed, puuid=summoner.puuid, match=match_history[0])
        Embed.match_mini(embed=embed, puuid=summoner.puuid, match=match_history[1])
        Embed.match_mini(embed=embed, puuid=summoner.puuid, match=match_history[2])
        Embed.match_mini(embed=embed, puuid=summoner.puuid, match=match_history[3])
        Embed.match_mini(embed=embed, puuid=summoner.puuid, match=match_history[4])
        return embed

    @staticmethod
    def profile_match(puuid: str, match: Match) -> discord.Embed:
        info = match.info
        queue = info.queue

        player = next((p for p in info.participants if p.puuid == puuid), info.participants[0])

        embed = discord.Embed(
            description=(
                f"# {queue.emoji_victory if player.win else queue.emoji_defeat} \u200b {Match.victory if player.win else Match.defeat}\n"
                f"**{queue.map} \u200b • \u200b {queue.description} \u200b • \u200b "
                f"{info.duration} \u200b • \u200b <t:{info.end_timestamp}:d> \u200b • \u200b ||{match.id.split('_')[1]}||**\n"
                f"```ansi\n{Color.ansi_gray}—————————————————————————————————————————————————————————————```"
            ),
            color=Color.victory if player.win else Color.defeat,
        )
        if info.teams[0].bans:
            bans_team_1_emoji = " ".join(ban.champion.get_emoji for ban in info.teams[0].bans)
            bans_team_2_emoji = " ".join(ban.champion.get_emoji for ban in info.teams[1].bans)
            embed.add_field(
                name="",
                value=f"{bans_team_1_emoji}{blank * 15}{bans_team_2_emoji}",
                inline=False,
            )
        Embed.match_team(embed=embed, team_id=100, team=info.teams[0], participants=info.participants[:5])
        Embed.match_team(embed=embed, team_id=200, team=info.teams[1], participants=info.participants[5:])
        return embed

    @staticmethod
    def profile_match_error() -> discord.Embed:
        return discord.Embed(
            description=(
                "## WE DIDN'T FIND ANY MATCHES FOR THIS PLAYER.\n"
                "### THIS MIGHT BE BECAUSE...\n"
                f"{blank}• This summoner hasn't played any ranked matches\n"
                f"{blank}• This summoner isn't fiends with the bot (and thus bot can't\n"
                f"{blank} \u200b  \u200b see their matches)\n"
                f"{blank}• This summoner hasn't played any matches since May 1st\n"
                f"{blank}\n{blank}\n{blank}\n"
            ),
            color=Color.error,
        ).set_author(
            name="MATCH COMMAND ERROR", icon_url=Icon.ux_x,
        ).set_thumbnail(
            url=Icon.random_poro(happy=False),
        )

#TODO: create embed for arena
