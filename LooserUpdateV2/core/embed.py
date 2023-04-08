import discord

from datetime import datetime, timedelta

from .resources import Emoji, Icon, Color
from .common import spacing, percent, opgg

from datastores.emoji import Item

class Format:
    """ Format data for embeds. """
    
    def rank(rank_data):
        """ Format the rank data. """
        if rank_data.get('tier'):
            tier, rank, wins, losses, lp = [rank_data.get(key) for key in ('tier', 'rank', 'wins', 'losses', 'leaguePoints')]
            value = (
                f"{Emoji.tier.get(tier, Emoji.tier['UNRANKED'])} "
                f"\u200b **{tier} {rank}**{spacing(tier, wins, losses)}{lp} LP\n"
                f"**Win Rate {percent(wins, losses)}%** {Emoji.blank} {wins}W / {losses}L\n{Emoji.blank}"
            )
        else:
            value = f"{Emoji.tier['UNRANKED']} \u200b **Unranked** \n{Emoji.blank}"
            
        return value

    def match_info(info, data):
        """ Formats information about a match into a string. """
        position = Emoji.position.get(data.get('position'), Emoji.position['FILL'])
        
        if data.get('win'):
            if info.get('gameMap') == 'Howling Abyss':
                map_emoji = Emoji.aram['victory']
            else:
                map_emoji = Emoji.sr['victory']
        else:
            if info.get('gameMap') == 'Howling Abyss':
                map_emoji = Emoji.aram['defeat']
            else:
                map_emoji = Emoji.sr['defeat']
        
        match_summoner = (
            f"{position} {info.get('gameDescription')}\n"
            f"{Emoji.champion.get(data.get('champion'), Emoji.champion['None'])} {Emoji.summoner[data.get('summonerSpells1')]} {Emoji.summoner[data.get('summonerSpells2')]}{Emoji.blank * 3}"
        )
        match_info = f"{info.get('gameMap')}\n{info.get('gameDuration')} \u200b  • \u200b <t:{info.get('gameEndTimestamp')}:R>"
        
        return map_emoji, match_summoner, match_info

    def match_stats(data):
        """ Formats data about a match into a string. """
        items   = [Item.get_emoji(item) for item in data.get('items')[:7]]
        kda     = f"{data.get('kills')} / {data.get('deaths')} / {data.get('assists')}"
        cs      = f"{data.get('cs')}{Emoji.history['cs']}"
        gold    = f"{data.get('gold')}{Emoji.history['gold']}"
        
        match_stats  = (
            f"{Emoji.blank}{' '.join(items)}\n"
            f"**{kda}{Emoji.blank}{cs}{Emoji.blank}{gold}**"
        )
        
        return match_stats
    
    def team(game_map, player_name, team_name, team_data, team_info):
        """ Formats data about a team into a string. """
        team_title  = f"**TEAM \u200b {team_name}{Emoji.blank}\u200b {team_info['kills']} \u200b / \u200b {team_info['deaths']} \u200b / \u200b {team_info['assists']} \u200b {Emoji.history['kda']}{Emoji.blank}**"
        items_title = f"{Emoji.blank * 2}{team_info['gold']} {Emoji.history['gold']}"
        stats_title = f"{Emoji.blank * 3}{Emoji.history['kda']}"
        
        team_value = items_value = stats_value = ""
        for player in team_data:
            position    = Emoji.position.get(player.get('position'), Emoji.position['FILL']) if game_map == "Summoner's Rift" else ""
            rune        = Emoji.rune.get(player.get('rune'), Emoji.rune['Runes'])
            name        = f"__*{player.get('name')}*__" if player.get('name') == player_name else player.get('name', '')
            level       = player.get('level', '1')
            champion    = Emoji.champion.get(player.get('champion'), Emoji.champion['None'])
            items       = [Item.get_emoji(player.get('items')[i]) for i in range(7)]
            
            team_value  += f'{position}{rune} **{level}** \u200b {champion} \u200b {name}\n'
            items_value += f"{' '.join(items)}\n"
            stats_value += f"{Emoji.blank} \u200b  \u200b **{player.get('kills')} \u200b / \u200b {player.get('deaths')} \u200b / \u200b {player.get('assists')}**\n"
        
        return team_title, team_value, items_title, items_value, stats_title, stats_value
    
    def bans_objectives(game_map, team_bans, team_objectives):
        """ Formats data about objectives into a string. """
        title = 'BANS \u200b + \u200b OBJECTIVES' if len(team_bans) > 0 else 'OBJECTIVES'
        
        bans = ""
        try:
            for i in range(5): bans += f"{Emoji.champion[team_bans[i]]}{Emoji.blank}"
        except:
            pass
        
        objectives = f"\n{Emoji.history['tower']} \u200b {team_objectives[0]}{Emoji.blank}{Emoji.history['inhibitor']} \u200b {team_objectives[1]}"
        if game_map == "Summoner's Rift":
            objectives += f"{Emoji.blank}{Emoji.history['baron']} \u200b {team_objectives[2]}{Emoji.blank}{Emoji.history['dragon']} \u200b {team_objectives[3]}{Emoji.blank}{Emoji.history['herald']} \u200b {team_objectives[4]}"
        objectives += f"\n{Emoji.blank}"
        
        return title, bans, objectives


class Field:
    """ Embed field. """
    
    def add_match(embed, match, is_last_match):
        """ Adds a field to the embed for a match. """
        info, data, *extra = match
        map_emoji, match_summoner, match_info = Format.match_info(info, data)
        match_stats = Format.match_stats(data)
        
        if is_last_match:
            match_summoner  += f"\n{Emoji.blank}"
            match_stats     += f"\n{Emoji.blank}"
            match_info      += f"\n{Emoji.blank}"
    
        embed.add_field(
            name        = f"{map_emoji} {'**VICTORY**' if data['win'] else '**DEFEAT**'}",
            value       = match_summoner,
            inline      = True
        )
        embed.add_field(
            name        = Emoji.blank,
            value       = match_stats,
            inline      = True
        )
        embed.add_field(
            name        = Emoji.blank,
            value       = match_info,
            inline      = True
        )
        
        return embed
            
    def add_team(embed, game_map, player_name, team_name, team_data, team_info, team_bans, team_objectives):
        """ Adds a field to the embed for a team. """
        team_title, team_value, items_title, items_value, stats_title, stats_value = Format.team(game_map, player_name, team_name, team_data, team_info)
        bans_objectives_title, bans, objectives = Format.bans_objectives(game_map, team_bans, team_objectives)
        
        embed.add_field(
            name        = team_title,
            value       = team_value,
            inline      = True
        )
        embed.add_field(
            name        = items_title,
            value       = items_value,
            inline      = True
        )
        embed.add_field(
            name        = stats_title,
            value       = stats_value,
            inline      = True
        )
        embed.add_field(
            name        = bans_objectives_title,
            value       = bans + objectives,
            inline      = False
        )
        
        return embed
    

class Embed:
    """ Embed for the bot """
        
    def success(message, description) -> discord.Embed:
        """ Create a Discord embed for the success command. """
        embed = discord.Embed(
            title       = f"```{message}```",
            description = f"**{description}**",
            color       = Color.default,
            timestamp   = datetime.utcnow()
        ).set_author(
            name        = "COMMAND SUCCESS",
            icon_url    = Icon.error
        ).set_thumbnail(
            url         = Icon.poro_mission
        )
        
        return embed

    def error(message) -> discord.Embed:
        """ Create a Discord embed for the error command. """
        description = "Something went horribly wrong executing that command, please try again in a bit. If this error keeps happening, please send a bug report.\n\nTry '/help' for more information."
        embed = discord.Embed(
            title       = f"```{message}```",
            description = description,
            color       = Color.error,
            timestamp   = datetime.utcnow()
        ).set_author(
            name        = "COMMAND ERROR",
            icon_url    = Icon.error
        ).set_image(
            url         = Icon.error_image
        )
        
        return embed
    
    def system(message, description) -> discord.Embed:
        """ Embed for system command error. """
        embed = discord.Embed(
            title       = f"```{message}```",
            description = f"**{description}**",
            color       = Color.error,
            timestamp   = datetime.utcnow()
        ).set_author(
            name        = "COMMAND ERROR",
            icon_url    = Icon.error
        ).set_thumbnail(
            url         = Icon.poro_error
        )
        
        return embed
    
    def help(commands) -> discord.Embed:
        """ Create a Discord embed for the help command. """
        embed = discord.Embed(
            title       = "List of commands",
            description = "",
            color       = Color.default,
            timestamp   = datetime.utcnow()
        ).set_author(
            name        = "HELP",
            icon_url    = Icon.book
        ).set_thumbnail(
            url         = Icon.poro_voice
        )

        # Add fields for each command
        for name, description in commands.items():
            embed.add_field(
                name    = name.capitalize(),
                value   = f"```{description}```",
                inline  = False
            )

        return embed
    
    def setting(region, players, max_players) -> discord.Embed:
        """ Create a Discord embed for the setting command. """
        embed = discord.Embed(
            title       = "Selected data will be the default value for profile, player to update.",
            description = "",
            color       = Color.default,
            timestamp   = datetime.utcnow()
        ).set_author(
            name        = "SETTINGS",
            icon_url    = Icon.setting
        )
        
        # Add region field
        embed.add_field(
            name        = "REGION",
            value       = f"```{region.value[0]} ({region.value[1]})```",
            inline      = False
        )
        
        # Add players field
        players_details = []
        for player in players:
            summoner    = player.get('summoner')
            league      = player.get('league')
            name        = summoner.get('name')
            region_code = player.get('region')
            division    = f"{league.get('tier')} {league.get('rank')}"
            lp          = league.get('leaguePoints')
            wins        = league.get('wins')
            losses      = league.get('losses')

            # Handle unranked players
            if league.get('tier') is None:
                player_details = f"```{name} #{region_code}\nUnranked```"
            else:
                win_rate = percent(wins, losses)
                player_details = f"```{name} #{region_code}\n{division} • {lp} LP | Win Rate {win_rate}% • [{wins}W / {losses}L]```"

            players_details.append(player_details)

        players_value = '\n'.join(players_details)
        if not players_value:
            players_value = "``` ```"

        embed.add_field(
            name        = f"PLAYER (Max. {max_players})",
            value       = players_value,
            inline      = False
        )
        
        return embed
    
    def region(region) -> discord.Embed:
        """ Create a Discord embed for the region command. """
        region = region.get('region')
        embed = discord.Embed(
            title       = f"```{region.value[1]} ({region.value[0]})```",
            description = "**Selected as default region.**",
            color       = Color.default,
            timestamp   = datetime.utcnow()
        ).set_author(
            name        = "COMMAND SUCCESS",
            icon_url    = Icon.error
        )
        
        return embed

    def summoner_profile(summoner_data, region_data, challenges_data, league_data, mastery_score_data, masteries_data) -> discord.Embed:
        """ Create a Discord embed for the summoner's profile. """
        summoner_name       = summoner_data.get('name')
        summoner_level      = summoner_data.get('level')
        summoner_icon_url   = summoner_data.get('profileIcon')
        region              = region_data.get('region').value[0]
        challenges_title    = challenges_data.get('title')
        solo_rank_data      = league_data.get('solo')
        flex_rank_data      = league_data.get('flex')
        champion_names      = masteries_data.get('championNames')[:3]
        champion_levels     = masteries_data.get('championLevels')[:3]
        champion_points     = masteries_data.get('championPoints')[:3]

        embed = discord.Embed(
            title       = f"**{summoner_name} \u200b #{region}**",
            url         = opgg(summoner_name, region),
            description = f"{summoner_level} \u200b | \u200b {challenges_title}" if challenges_title else str(summoner_level),
            color       = Color.default,
        ).set_author(
            name        = "Summoner \u200b Profile \u200b \u200b • \u200b \u200b OVERVIEW",
            icon_url    = Icon.nav_profile
        ).set_thumbnail(
            url         = summoner_icon_url
        )

        # Add Rank Solo/Duo & Flex fields
        for queue_type, rank_data in [('SOLO/DUO', solo_rank_data), ('FLEX 5V5', flex_rank_data)]:
            embed.add_field(
                name    = queue_type,
                value   = Format.rank(rank_data),
                inline  = True
            )

        # Add Mastery Score field
        embed.add_field(
            name        = "MASTERY \u200b SCORE",
            value       = f"{Emoji.mastery['default']} \u200b **{mastery_score_data}**\n{Emoji.blank}",
            inline      = False
        )

        # Add Champions Masteries fields
        champion_mastery_fields = []
        for champion_name, champion_level, champion_point in zip(champion_names, champion_levels, champion_points):
            champion_mastery_field = (
                f"{Emoji.mastery[champion_level]} \u200b {Emoji.champion.get(champion_name, Emoji.champion['None'])} \u200b **{champion_name.upper()}** \n"
                f"{Emoji.mastery['default']} \u200b {champion_point} pts \n{Emoji.blank}"
            )
            champion_mastery_fields.append(champion_mastery_field)

        for i, field_name in enumerate(['HIGHEST', 'CHAMPION', 'SCORE']):
            embed.add_field(
                name    = field_name,
                value   = champion_mastery_fields[i],
                inline  = True
            )
            
        return embed

    def summoner_history(history_data) -> discord.Embed:
        """ Creates an embed for the match history of a summoner. """
        embed = discord.Embed(
            title       = "RECENT \u200b GAMES \u200b (LAST 5 PLAYED)",
            description = '',
            color       = Color.default
        ).set_author(
            name        = "Summoner \u200b Profile \u200b \u200b • \u200b \u200b MATCH \u200b HISTORY",
            icon_url    = Icon.nav_profile
        )

        for match in history_data:
            Field.add_match(embed, match, match == history_data[-1])
        
        return embed

    def summoner_history_light(match, player):
        """ Creates an embed for a match in the match history of a summoner. """
        region          = player.get('region')
        summoner        = player.get('summoner')
        name            = summoner.get('name')
        profile_icon    = summoner.get('profileIcon')
        league          = player.get('league')
        tier            = league.get('tier')
        rank            = league.get('rank')
        lp              = league.get('leaguePoints')
        wins            = league.get('wins')
        losses          = league.get('losses')
        resume          = player.get('resume')

        if tier:
            description = (
                f"{Emoji.tier[tier]} \u200b **{tier} \u200b {rank}**{Emoji.blank}{lp} LP \u200b `{resume}`"
                f"**{Emoji.blank}•{Emoji.blank}Win Rate \u200b {percent(wins, losses)}%**{Emoji.blank}{wins}W / {losses}L\n{Emoji.blank}"
            )
        else:
            description = (
                f"{Emoji.tier['UNRANKED']} \u200b **Unranked**{Emoji.blank}"
                f"`{resume}`\n{Emoji.blank}"
            )

        embed = discord.Embed(
            title       = f"{name} \u200b #{region}",
            url         = opgg(name, region),
            description = description,
            color       = Color.victory if match[1]['win'] else Color.defeat,
            timestamp   = datetime.utcnow()
        ).set_author(
            name        = f"Summoner \u200b Profile \u200b \u200b • \u200b \u200b {name.upper()}",
            icon_url    = profile_icon
        ).set_footer(
            text        = "LooserUpdateV2",
            icon_url    = Icon.emrata
        )
        Field.add_match(embed, match, True)
        
        return embed

    def match(match):
        """ Creates an embed for a match in the match history of a summoner. """
        win = "VICTORY" if match[1]["win"] else "DEFEAT"
        
        icon_map = (
            Icon.ha_victory if match[0]["gameMap"] == "Howling Abyss" else Icon.sr_victory
        ) if match[1]["win"] else (
            Icon.ha_defeat if match[0]["gameMap"] == "Howling Abyss" else Icon.sr_defeat
        )
        
        title = f"{match[0]['gameMap']} \u200b • \u200b {match[0]['gameDescription']} \u200b • \u200b {match[0]['gameDuration']} \u200b • \u200b <t:{match[0]['gameEndTimestamp']}:d>"
        embed = discord.Embed(
            title       = title,
            description = "",
            color       = Color.victory if match[1]["win"] else Color.defeat
        ).set_author(
            name        = win,
            icon_url    = icon_map
        )
        
        Field.add_team(embed, match[0]['gameMap'], match[1]['name'], '1', match[2], match[4], match[6], match[8])
        Field.add_team(embed, match[0]['gameMap'], match[1]['name'], '2', match[3], match[5], match[7], match[9])

        return embed

    def error_match(message, description) -> discord.Embed:
        """ Embed for match command error. """
        embed = discord.Embed(
            title       = message,
            description = f"**{description}**",
            color       = Color.error,
            timestamp   = datetime.utcnow()
        ).set_author(
            name        = "COMMAND ERROR",
            icon_url    = Icon.error
        ).set_thumbnail(
            url         = Icon.poro_error
        )
        
        return embed
    