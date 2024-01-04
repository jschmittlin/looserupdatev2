from typing import Union, List
import discord

from .account import Account
from .summoner import Summoner
from .match import Match, MatchHistory
from .player import Player, PlayerList
from .challenges import PlayerInfo
from .championmastery import ChampionMasteries
from .league import LeagueEntries
from ..data import Region, Platform, Queue, Tier, Lane

from ..resources import Icon, Color 
from ..resources.emoji import blank, Mastery, Match


space = " \u200b "
split = " \u200b • \u200b "

def blitz_profile(game_name: str, tag_line: str, platform: Platform) -> str:
    try:
        return "https://blitz.gg/lol/profile/{platform}/{game_name}-{tag_line}".format(
            platform=platform.value.lower(), game_name=game_name.replace(' ', '%20'), tag_line=tag_line,
        )
    except Exception:
        return "https://blitz.gg"

def blitz_match(game_name: str, tag_line: str, platform: Platform, id: str) -> str:
    try:
        return "https://blitz.gg/lol/match/{platform}/{game_name}-{tag_line}/{id}".format(
            platform=platform.value.lower(), game_name=game_name.replace(' ', '%20'), tag_line=tag_line, id=id,
        )
    except Exception:
        return "https://blitz.gg"

def opgg(game_name: str, tag_line: str, region: str) -> str:
    try:
        return "https://www.op.gg/summoners/{region}/{game_name}-{tag_line}".format(
            region=region.value.lower(), game_name=game_name.replace(' ', '%20'), tag_line=tag_line,
        )
    except Exception:
        return "https://www.op.gg"

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

def spacing_lane(position: Lane) -> str:
    if position == Lane.top:
        return space * 2
    if position == Lane.jungle:
        return ""
    if position == Lane.middle:
        return space * 2
    if position == Lane.bottom:
        return space * 2
    if position == Lane.utility:
        return ""
    if position == Lane.fill:
        return blank
    if position == Lane.unselected:
        return blank

def spacing_queue(queue: Queue) -> str:
    if queue == Queue.normal_draft_five:
        return ""
    if queue == Queue.ranked_solo_five:
        return ""
    if queue == Queue.ranked_flex_five:
        return space * 4
    if queue == Queue.aram:
        return blank * 4 + space * 2
    if queue == Queue.cherry:
        return blank * 4 + space * 2

def get_cherry_team(id: int, placement: int) -> str:
    team_names = {
        1: (Match.poro, Match.poro_title),
        2: (Match.minion, Match.minion_title),
        3: (Match.scuttle, Match.scuttle_title),
        4: (Match.krug, Match.krug_title),
    }
    team_positions = {
        1: (Match.poro_1st, Match.minion_1st, Match.scuttle_1st, Match.krug_1st),
        2: (Match.poro_2nd, Match.minion_2nd, Match.scuttle_2nd, Match.krug_2nd),
        3: (Match.poro_3rd, Match.minion_3rd, Match.scuttle_3rd, Match.krug_3rd),
        4: (Match.poro_4th, Match.minion_4th, Match.scuttle_4th, Match.krug_4th),
    }
    team_name, team_title = team_names[id]
    team_position = team_positions[placement][id - 1]
    return f"{team_position}{team_name} {team_title}" if team_name else ""

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
        for command in commands:
            embed.add_field(
                name=f"/{command.name}",
                value=f"```{command.description}```",
                inline=False,
            )
        return embed

    @staticmethod
    def region_edit(region: Union[Region, str]) -> discord.Embed:
        if not isinstance(region, Region): region = Region(region)
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
                f"{Color.discord_preset_player(game_name=player.game_name, tag_line=player.tag_line)}\n"
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
                f"{Color.discord_preset_player(game_name=player.game_name, tag_line=player.tag_line)}\n"
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
            f"{Color.ansi_white}{Color.ansi_bold}{player.game_name} {Color.ansi_gray}#{player.tag_line}\n"
            f"{f'{player.tier.color}{player.tier} {player.division.value} {Color.ansi_reset}(Solo/Duo)' if player.tier else f'{Tier.unranked.color}{Tier.unranked}'}"
            f"```"
            for player in players
        ]) or "``` ```"

        embed.add_field(
            name=f"**PLAYER MANAGE (MAX PLAYER {players._max_size})**{blank * 6}",
            value=players_value,
            inline=False,
        )

        return embed

    @staticmethod
    def player_update(player: Player, match: Match) -> discord.Embed:
        match_player = next((p for p in match.participants if p.puuid == player.puuid), match.participants[0])

        player_rank = f"{player.tier} {player.division.value}" if player.tier else f"{Tier.unranked}"
        player_rank_color = player.tier.color if player.tier else Tier.unranked.color

        result_color = Color.ansi_blue if match_player.win else Color.ansi_red
        league_points = f"{player.league_points} LP"

        winrate = f"{get_winrate(player.wins, player.losses)}% Win Rate"
        win_loss = f"{player.wins}W - {player.losses}L"

        rank_padding = 61 - (len(player_rank) + len(league_points) + len(player.description) + 3)
        win_padding = 61 - (len(win_loss) + len(winrate))

        embed_description = (
            f"```ansi\n"
            f"{player_rank_color}{player_rank}{' ' * rank_padding}{result_color}"
            f"{player.description}{Color.ansi_gray} • {Color.ansi_reset}{league_points}"
            f"\n{Color.ansi_gray}"
            f"{winrate}{' ' * win_padding}{win_loss}"
            f"```{blank}"
        )

        embed = discord.Embed(
            description=embed_description,
            color=Color.victory if match_player.win else Color.defeat,
        ).set_author(
            name=f"{player.game_name} #{player.tag_line}",
            icon_url=player.profile_icon.url,
            url=blitz_profile(game_name=player.game_name, tag_line=player.tag_line, platform=player.platform),
        )

        Embed.match_mini(embed=embed, puuid=player.puuid, match=match)

        return embed

    @staticmethod
    def error_summoner(error: str) -> discord.Embed:
        return discord.Embed(
            description=(
                f"{Color.discord_preset_error(error=error)}\n"
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
    def profile_overview(
        summoner: Summoner, account: Account, challenges: PlayerInfo, masteries: ChampionMasteries, league: LeagueEntries
    ) -> discord.Embed:
        title = f'*{challenges.preferences.title.title}*\n' if challenges.preferences.title.title else ''

        embed = discord.Embed(
            description=(
                f"{Mastery.mastery} **{masteries.score}**{blank * 16}Lvl.{summoner.level}\n"
                f"{title}"
                f"```ansi\n{Color.ansi_gray}—————————————————————————————————————————————————```"
            ),
            color=Color.default,
        ).set_author(
            name=f"{account.game_name} #{account.tag_line}",
            icon_url=summoner.profile_icon.url,
            url=blitz_profile(game_name=account.game_name, tag_line=account.tag_line, platform=summoner.platform),
        ).set_thumbnail(
            url=summoner.profile_icon.url,
        ).set_footer(
            text=summoner.region, icon_url=summoner.region.icon,
        )

        def league_field(embed: discord.Embed, league: LeagueEntries, type: str) -> None:
            try:
                if type == "SOLO/DUO":
                    league = league.solo
                if type == "FLEX":
                    league = league.flex
            except ValueError:
                embed.add_field(
                    name=f"**{type}**",
                    value=f"{Tier.unranked.emoji} `{Tier.unranked}`\n{blank * 10}",
                    inline=True,
                )
            else:
                rank = f"{league.tier} {league.division.value}"
                lp = f"{league.league_points} LP"
                win_loss = f"{league.wins}W - {league.losses}L"

                length_lp = 25 - (len(rank) + len(lp))
                length_win_loss = 16 - len(win_loss)

                spacing_lp = f"{space * 2}" * length_lp
                spacing_win_loss = f"{space * 2}" * length_win_loss

                embed.add_field(
                    name=f"**{type}**",
                    value=(
                        f"{league.tier.emoji} `{rank}`{spacing_lp}{lp}\n"
                        f"{get_winrate(league.wins, league.losses)}% Win Rate{spacing_win_loss}{win_loss}\n"
                        f"{blank * 10}"
                    ),
                    inline=True,
                )
            

        league_field(embed=embed, league=league, type="SOLO/DUO")
        league_field(embed=embed, league=league, type="FLEX")

        masteries_fields = []
        for mastery in masteries.champion_mastery_list:
            length_diff = 13 - len(mastery.champion.name)
            spacing = f"{space * 2}" * length_diff
            s = f"{mastery.champion.get_emoji} `{mastery.champion.name}`{spacing}{Mastery.mastery} {mastery.points:,} pts"
            masteries_fields.append(s)

        embed.add_field(
            name="**HIGHEST CHAMPION MASTERY**",
            value="\n".join(masteries_fields) + blank,
            inline=False,
        )

        return embed

    @staticmethod
    def mini_classic_aram(embed: discord.Embed, match: "Match", player: "Participant") -> None:
        queue = match.queue
        win = Match.remake if player.remake else (Match.victory if player.win else Match.defeat)
        map_emoji = queue.emoji_victory if player.win else queue.emoji_defeat
        items_emoji = " ".join(item.get_emoji for item in player.items)
        position_emoji = f"{player.position.emoji_hover} {player.position}"

        field_2_blank = spacing_lane(player.position) + spacing_queue(queue)
        
        embed.add_field(
            name=f"**{map_emoji}{space * 2}{win}**",
            value=(
                f"{player.champion.get_emoji}"
                f"{blank}"
                f"{player.spell_d.get_emoji} {player.spell_f.get_emoji}\n"
                f"**{player.kills} / {player.deaths} / {player.assists}**"
            ),
            inline=True,
        )
        embed.add_field(
            name=f"**{field_2_blank}{position_emoji}{split}{queue.description}**",
            value=(
                f"{player.runes[0].get_emoji}"
                f"{blank}{items_emoji}\n"
                f"{Match.sword} **{player.damage_dealt:,}**"
                f"{space * 3}"
                f"{Match.shield} **{player.damage_taken:,}**"
                f"{space * 3}"
                f"{Match.cc} **{player.crowd_control:,}**"
            ),
            inline=True,
        )
        embed.add_field(
            name=f"**•{space}{queue.map}**",
            value=(
                f"**{match.duration}{split}"
                f"<t:{match.end}:R>**\n"
                f"{Match.minions} **{player.creep_score:,}**"
                f"{blank}{Match.gold} **{player.gold:,}**"
            ),
            inline=True,
        )

    @staticmethod
    def mini_cherry(embed: discord.Embed, match: "Match", player: "Participant") -> None:
        queue = match.queue
        
        field_2_blank = spacing_lane(Lane.fill) + spacing_queue(queue)
        items_emoji = " ".join(item.get_emoji for item in player.items)
        augments_emoji = " ".join(augment.get_emoji for augment in player.augments)

        embed.add_field(
            name=get_cherry_team(id=player.subteam_id, placement=player.subteam_placement),
            value=(
                f"{player.champion.get_emoji}"
                f"{blank}"
                f"{player.spell_d.get_emoji} {player.spell_f.get_emoji}\n"
                f"**{player.kills} / {player.deaths} / {player.assists}**"
            ),
            inline=True,
        )
        embed.add_field(
            name=f"**{field_2_blank}{Lane.fill.emoji_hover}{split}{queue.description}**",
            value=(
                f"{blank * 2}{items_emoji}\n"
                f"{Match.sword}**{player.damage_dealt:,}**"
                f"{space * 2}"
                f"{Match.shield}**{player.damage_taken:,}**"
                f"{space * 2}"
                f"{Match.cc}**{player.crowd_control:,}**"
            ),
            inline=True,
        )
        embed.add_field(
            name=f"**•{space}{match.duration}{split}<t:{match.end}:R>**",
            value=(
                f"{augments_emoji}\n"
                f"{Match.minions} **{player.creep_score:,}**"
                f"{blank}{Match.gold} **{player.gold:,}**"
            ),
            inline=True,
        )

    @staticmethod
    def match_mini(embed: discord.Embed, puuid: str, match: Match) -> None:
        queue = match.queue

        player = next((p for p in match.participants if p.puuid == puuid), match.participants[0])

        if queue == Queue.cherry:
            Embed.mini_cherry(embed=embed, match=match, player=player)
        else:
            Embed.mini_classic_aram(embed=embed, match=match, player=player)

    @staticmethod
    def profile_match_history(matchs: List[Match], puuid: str) -> discord.Embed:
        embed = discord.Embed(
            description=(
                f"### RECENT GAMES (LAST 5 PLAYED)\n"
                f"```ansi\n{Color.ansi_gray}—————————————————————————————————————————————————————————————```"
            ),
            color=Color.default,
        )
        Embed.match_mini(embed=embed, puuid=puuid, match=matchs[0])
        Embed.match_mini(embed=embed, puuid=puuid, match=matchs[1])
        Embed.match_mini(embed=embed, puuid=puuid, match=matchs[2])
        Embed.match_mini(embed=embed, puuid=puuid, match=matchs[3])
        Embed.match_mini(embed=embed, puuid=puuid, match=matchs[4])
        return embed

    @staticmethod
    def classic_team(embed: discord.Embed, team_id: int, team: "Team", participants: List["Participant"]) -> None:
        objectives = team.objectives

        field_1_value = field_2_value = field_3_value = ""
        total_kills = total_deaths = total_assists = total_gold = 0

        for participant in participants:
            total_kills += participant.kills
            total_deaths += participant.deaths
            total_assists += participant.assists
            total_gold += participant.gold

            name = participant.riot_game_name
            truncated_name = name[:12] + "..." if len(name) > 15 else name
            champion_emoji = participant.champion.get_emoji
            champion_level = f"`{participant.level}`" if participant.level > 9 else f"\u200b `{participant.level}` \u200b "
            kda = f"{participant.kills} / {participant.deaths} / {participant.assists}"
            items_emoji = " ".join(item.get_emoji for item in participant.items)
            main_rune_emoji = participant.runes[0].get_emoji
            dmg = f"`{participant.damage_dealt:,} DMG`" if participant.damage_dealt > 10000 else f"` {participant.damage_dealt:,} DMG`"

            kda_blank = " "
            if participant.kills < 10:
                kda_blank += "\u200b \u200b "
            if participant.deaths < 10:
                kda_blank += "\u200b \u200b "
            if participant.assists < 10:
                kda_blank += "\u200b \u200b "
            kda_blank = kda_blank[:int(len(kda_blank)/2)] + f"`{kda}`" + kda_blank[int(len(kda_blank)/2):]

            field_1_value += f"{main_rune_emoji} {champion_emoji} {champion_level} `{truncated_name}`\n"
            field_2_value += f"{items_emoji}\n"
            field_3_value += f"{kda_blank}{dmg}\n"

        embed.add_field(
            name=f"{Match.team1 if team_id == 100 else Match.team2}{blank * 2}{total_kills} / {total_deaths} / {total_assists}",
            value=field_1_value,
            inline=True,
        )
        embed.add_field(
            name=(
                f"{space}{blank}{space}"
                f"{Match.baron} {objectives.baron.kills}{space}"
                f"{Match.herald} {objectives.rift_herald.kills}{space}"
                f"{Match.dragon} {objectives.dragon.kills}"
            ),
            value=field_2_value,
            inline=True,
        )
        embed.add_field(
            name=(
                f"{Match.tower} {objectives.tower.kills}{space}"
                f"{Match.inhibitor} {objectives.inhibitor.kills}{blank}"
                f"{Match.gold} {total_gold}"
            ),
            value=field_3_value,
            inline=True,
        )

    @staticmethod
    def classic_aram_match(embed: discord.Embed, match: "Match") -> None:
        team_1_bans = " ".join(ban.champion.get_emoji for ban in match.teams[0].bans)
        team_2_bans = " ".join(ban.champion.get_emoji for ban in match.teams[1].bans)

        if team_1_bans or team_2_bans:
            embed.add_field(
                name="", value=f"{team_1_bans}{blank * 15}{team_1_bans}", inline=False,
            )

        Embed.classic_team(embed=embed, team_id=100, team=match.teams[0], participants=match.participants[:5])
        Embed.classic_team(embed=embed, team_id=200, team=match.teams[1], participants=match.participants[5:])

    @staticmethod
    def cherry_team(embed: discord.Embed, participants: List["Participant"]) -> None:
        field_1_value = field_2_value = field_3_value = ""
        total_kills = total_deaths = total_assists = total_gold = 0
        subteam_id = subteam_placement = 0

        for participant in participants:
            total_kills += participant.kills
            total_deaths += participant.deaths
            total_assists += participant.assists
            total_gold += participant.gold

            subteam_id = participant.subteam_id
            subteam_placement = participant.subteam_placement

            champion_emoji = participant.champion.get_emoji
            spell_d_emoji = participant.spell_d.get_emoji
            spell_f_emoji = participant.spell_f.get_emoji
            name = participant.riot_game_name
            truncated_name = name[:10] + "..." if len(name) > 13 else name
            items_emoji = " ".join(item.get_emoji for item in participant.items)
            augments_emoji = "".join(augment.get_emoji for augment in participant.augments)
            kda = f"{participant.kills} / {participant.deaths} / {participant.assists}"
            dmg = f"`{participant.damage_dealt:,} DMG`" if participant.damage_dealt > 10000 else f"` {participant.damage_dealt:,} DMG`"

            kda_blank = " "
            if participant.kills < 10:
                kda_blank += "\u200b \u200b "
            if participant.deaths < 10:
                kda_blank += "\u200b \u200b "
            if participant.assists < 10:
                kda_blank += "\u200b \u200b "
            kda_blank = kda_blank[:int(len(kda_blank)/2)] + f"`{kda}`" + kda_blank[int(len(kda_blank)/2):]

            field_1_value += f"{champion_emoji}{space * 3}{spell_d_emoji} {spell_f_emoji}{space}`{truncated_name}`\n"
            field_2_value += f"{items_emoji}\n"
            field_3_value += f"{augments_emoji} {kda_blank}\n"

        embed.add_field(
            name=get_cherry_team(id=subteam_id, placement=subteam_placement),
            value=field_1_value,
            inline=True,
        )
        embed.add_field(
            name=f"{blank * 2}{space * 3}{total_kills} / {total_deaths} / {total_assists}",
            value=field_2_value,
            inline=True,
        )
        embed.add_field(
            name=f"{blank * 4}{space * 2}{Match.gold} {total_gold}",
            value=field_3_value,
            inline=True,
        )

    @staticmethod
    def cherry_match(embed: discord.Embed, match: "Match") -> None:
        bans = " ".join(ban.champion.get_emoji for ban in match.teams[0].bans)

        embed.add_field(
            name="", value=f"{bans}", inline=False,
        )

        teams = [
            (match.participants[0], match.participants[1]),
            (match.participants[2], match.participants[3]),
            (match.participants[4], match.participants[5]),
            (match.participants[6], match.participants[7]),
        ]

        placements = set(participant.subteam_placement for participant in match.participants)

        pairs = [team for placement in sorted(placements) for team in teams if team[0].subteam_placement == team[1].subteam_placement == placement]

        for pair in pairs:
            Embed.cherry_team(embed=embed, participants=pair)

    @staticmethod
    def profile_match(puuid: str, match: Match) -> discord.Embed:
        queue = match.queue

        player = next((p for p in match.participants if p.puuid == puuid), match.participants[0])
        win_text = Match.remake if player.remake else (Match.victory if player.win else Match.defeat)

        embed = discord.Embed(
            description=(
                f"# {queue.emoji_victory if player.win else queue.emoji_defeat}{space}{win_text}\n"
                f"**{queue.map}{split}{queue.description}{split}{match.duration}{split}<t:{match.end}:d>{split}"
                f"||[{match.id}]({blitz_match(player.riot_game_name, player.riot_tag_line, match.platform, match.id)})||**\n"
                f"```ansi\n{Color.ansi_gray}—————————————————————————————————————————————————————————————```"
            ),
            color=Color.victory if player.win else Color.defeat,
        )
        
        if queue == Queue.cherry:
            Embed.cherry_match(embed=embed, match=match)
        else:
            Embed.classic_aram_match(embed=embed, match=match)
        
        return embed

    @staticmethod
    def profile_match_error() -> discord.Embed:
        return discord.Embed(
            description=(
                "## WE DIDN'T FIND ANY MATCHES FOR THIS PLAYER.\n"
                "### THIS MIGHT BE BECAUSE...\n"
                f"{blank}• This summoner hasn't played any ranked matches\n"
                f"{blank}• This summoner isn't fiends with the bot (and thus bot can't\n"
                f"{blank}{space * 2}see their matches)\n"
                f"{blank}• This summoner hasn't played any matches since May 1st\n"
                f"{blank}\n{blank}\n{blank}\n"
            ),
            color=Color.error,
        ).set_author(
            name="MATCH COMMAND ERROR", icon_url=Icon.ux_x,
        ).set_thumbnail(
            url=Icon.random_poro(happy=False),
        )
