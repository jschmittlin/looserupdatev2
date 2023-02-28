import datetime
from datetime import datetime, timedelta

# Discord bot
import discord
from discord import Embed
from discord.ui import View, button, Select

# Resources
from resources import Emoji, Icon, Color

# Data
from data import Item


def replace_spaces(string: str):
    """ replace spaces with underscores """
    return string.replace(' ', '%20')

def percent(wins: int, losses: int):
    """ calculate the winrate """
    return round((wins / (wins + losses)) * 100)

def spacing(tier: str, wins: int, losses: int):
    """ calculate the spacing between the rank and the winrate """
    spaces = ""
    if tier == 'IRON' or tier == 'GOLD': spaces = f'{Emoji.blank}{Emoji.blank}{Emoji.blank} \u200b \u200b '
    if tier == 'BRONZE' or tier == 'SILVER' or tier == 'MASTER': spaces = f'{Emoji.blank}{Emoji.blank}{Emoji.blank}'
    if tier == 'PLATINUM' or tier == 'DIAMOND': spaces = f'{Emoji.blank} \u200b \u200b \u200b '
    if tier == 'GRANDMASTER' or tier == 'CHALLENGER': return f'{Emoji.blank}'
    if wins > 99: spaces += ' \u200b '
    if losses > 99: spaces += ' \u200b '
    return spaces


class MyEmbed:
    """ Embed for the bot """
    def __init__(self):
        super().__init__()
        self.embed_profile = None
        self.embed_history = None
        self.embed_history_light = None

    def init_data(self, region, summoner, league, mastery_score, masteries, challenges, history, match):
        self.region = region.get('region').value[0]
        self.name = summoner.get('name')
        self.level = summoner.get('level')
        self.icon = summoner.get('profileIcon')
        self.solo = league.get('solo')
        self.flex = league.get('flex')
        self.mastery_score = mastery_score
        self.masteries = masteries
        self.challenges = challenges
        self.history = history
        self.match = match

    def profile_embed(self):
        """ profile embed """
        if self.challenges.get('title') is not None:
            description = f'{self.level} \u200b | \u200b {self.challenges.get("title")}'
        else:
            description = f'{self.level}'
        
        try:
            opgg = f'https://www.op.gg/summoners/{self.region}/{replace_spaces(self.name)}'
        except:
            opgg = f'https://www.op.gg/'

        embed = discord.Embed(
            title=f'**{self.name} \u200b #{self.region}**',
            url=opgg,
            description=description,
            color=Color.default,
        )
        embed.set_author(
            name=f'Summoner \u200b Profile \u200b \u200b • \u200b \u200b OVERVIEW',
            icon_url=Icon.nav_profile
        )
        embed.set_thumbnail(url=self.icon)

        # Rank Solo/Duo & Flex
        value_solo = f'{Emoji.tier["UNRANKED"]} \u200b **Unranked** \n{Emoji.blank}'
        value_flex = f'{Emoji.tier["UNRANKED"]} \u200b **Unranked** \n{Emoji.blank}'

        if self.solo.get('tier') is not None:
            tier = self.solo.get('tier')
            rank = self.solo.get('rank')
            wins = self.solo.get('wins')
            losses = self.solo.get('losses')
            lp = self.solo.get('leaguePoints')
            spaces_solo = spacing(tier, wins, losses)
            value_solo = f"{Emoji.tier[tier]} \u200b **{tier} {rank}**{spaces_solo}{lp} LP\n"
            value_solo += f"**Win Rate {percent(wins, losses)}%** {Emoji.blank} {wins}W / {losses}L\n{Emoji.blank}"

        if self.flex.get('tier') is not None:
            tier = self.flex.get('tier')
            rank = self.flex.get('rank')
            wins = self.flex.get('wins')
            losses = self.flex.get('losses')
            lp = self.flex.get('leaguePoints')
            spaces_flex = spacing(tier, wins, losses)
            value_flex = f"{Emoji.tier[tier]} \u200b **{tier} {rank}**{spaces_flex}{lp} LP\n"
            value_flex += f"**Win Rate {percent(wins, losses)}%** {Emoji.blank} {wins}W / {losses}L\n{Emoji.blank}"

        embed.add_field(name='SOLO/DUO', value=value_solo, inline=True)
        embed.add_field(name='FLEX 5V5', value=value_flex, inline=True)

        # Mastery Score
        embed.add_field(
            name='MASTERY \u200b SCORE',
            value=f'{Emoji.mastery["default"]} \u200b **{self.mastery_score}**\n{Emoji.blank}',
            inline=False
        )

        # Champions Masteries
        champion_masteries = []
        for i in range(3):
            champion_name = self.masteries.get('championNames')[i]
            champion_level = self.masteries.get('championLevels')[i]
            champion_point = self.masteries.get('championPoints')[i]
            champion_mastery = f'{Emoji.mastery[champion_level]} \u200b {Emoji.champion[champion_name]} \u200b **{champion_name.upper()}** \n'
            champion_mastery += f'{Emoji.mastery["default"]} \u200b {champion_point} pts \n{Emoji.blank}'
            champion_masteries.append(champion_mastery)

        embed.add_field(name='HIGHEST', value=champion_masteries[0], inline=True)
        embed.add_field(name='CHAMPION', value=champion_masteries[1], inline=True)
        embed.add_field(name='SCORE', value=champion_masteries[2], inline=True)

        self.embed_profile = embed
        return embed

    def history_embed(self):
        """ history embed """
        embed = discord.Embed(
            title=f'RECENT \u200b GAMES \u200b (LAST 5 PLAYED)',
            description='',
            color=Color.default
        )
        embed.set_author(
            name=f'Summoner \u200b Profile \u200b \u200b • \u200b \u200b MATCH \u200b HISTORY',
            icon_url=Icon.nav_profile
        )

        for match in self.history:
            info = match[0]
            data = match[1]

            if data['win']:
                win = '**VICTORY**'
                if info['gameMap'] == 'Howling Abyss': emoji_map = Emoji.aram['victory']
                else: emoji_map = Emoji.sr['victory']
            else:
                win = '**DEFEAT**'
                if info['gameMap'] == 'Howling Abyss': emoji_map = Emoji.aram['defeat']
                else: emoji_map = Emoji.sr['defeat']

            try:
                position = Emoji.position[data['position']]
            except:
                position = Emoji.position['FILL']

            match_100 = f'{position} {info["gameDescription"]}\n'
            match_100 += f'{Emoji.champion[data["champion"]]} {Emoji.summoner[data["summonerSpells1"]]} {Emoji.summoner[data["summonerSpells2"]]}'
            match_100 += f'{Emoji.blank}{Emoji.blank}{Emoji.blank}'
            
            match_001 = f'{info["gameMap"]}\n{info["gameDuration"]} \u200b  • \u200b <t:{info["gameEndTimestamp"]}:d>'
                
            items = [Item.get_emoji(data["items"][i]) for i in range(7)]
            match_010 = f"{Emoji.blank}{' '.join(items)}\n"
            match_010 += f'**{data["kills"]} / {data["deaths"]} / {data["assists"]}{Emoji.blank}{data["cs"]}{Emoji.history["cs"]}{Emoji.blank}{data["gold"]}{Emoji.history["gold"]}**'

            if match == self.history[-1]:
                match_100 += f'\n{Emoji.blank}'
                match_010 += f'\n{Emoji.blank}'
                match_001 += f'\n{Emoji.blank}'

            embed.add_field(name=f'{emoji_map} {win}', value=match_100, inline=True)
            embed.add_field(name=Emoji.blank, value=match_010, inline=True)
            embed.add_field(name=Emoji.blank, value=match_001, inline=True)

        self.embed_history = embed
        return embed

    def history_light_embed(self, match, player):
        """ history embed (1 match) """
        region = player.get('region')
        name = player.get('summoner').get('name')
        profile_icon = player.get('summoner').get('profileIcon')
        tier = player.get('league').get('tier')
        rank = player.get('league').get('rank')
        lp = player.get('league').get('leaguePoints')
        wins = player.get('league').get('wins')
        losses = player.get('league').get('losses')
        resume = player.get('resume')

        try:
            opgg = f'https://www.op.gg/summoners/{region}/{replace_spaces(name)}'
        except:
            opgg = f'https://www.op.gg/'

        title = f'{name} \u200b #{region}'
        try:
            desc = f'{Emoji.tier[tier]} \u200b **{tier} \u200b {rank}**{Emoji.blank}{lp} LP \u200b `{resume}`'
            desc += f'**{Emoji.blank}•{Emoji.blank}Win Rate \u200b {percent(wins, losses)}%**{Emoji.blank}{wins}W / {losses}L\n{Emoji.blank}'
        except Exception as error:
            desc = f'{Emoji.tier["UNRANKED"]} \u200b **Unranked**{Emoji.blank}`{resume}`\n{Emoji.blank}'

        if match[1]['win']:
            color = Color.victory
        else:
            color = Color.defeat

        embed = discord.Embed(
            title=title,
            description=desc,
            url=opgg,
            color=color,
            timestamp=datetime.utcnow()
        )
        embed.set_author(
            name=f'Summoner \u200b Profile \u200b \u200b • \u200b \u200b {name.upper()}',
            icon_url=profile_icon
        )
        embed.set_footer(text="LooserUpdateV2", icon_url=Icon.emrata)

        info = match[0]
        data = match[1]

        if data['win']:
            win = '**VICTORY**'
            if info['gameMap'] == 'Howling Abyss': emoji_map = Emoji.aram['victory']
            else: emoji_map = Emoji.sr['victory']
        else:
            win = '**DEFEAT**'
            if info['gameMap'] == 'Howling Abyss': emoji_map = Emoji.aram['defeat']
            else: emoji_map = Emoji.sr['defeat']

        try: position = Emoji.position[data['position']]
        except: position = Emoji.position['FILL']

        match_100 = f'{position} {info["gameDescription"]}\n'
        match_100 += f'{Emoji.champion[data["champion"]]} {Emoji.summoner[data["summonerSpells1"]]} {Emoji.summoner[data["summonerSpells2"]]}'
        match_100 += f'{Emoji.blank}{Emoji.blank}{Emoji.blank}\n{Emoji.blank}'
        match_001 = f'{info["gameMap"]}\n{info["gameDuration"]} \u200b  • \u200b <t:{info["gameEndTimestamp"]}:d>\n{Emoji.blank}'
            
        items = [Item.get_emoji(data["items"][i]) for i in range(7)]
        match_010 = f"{Emoji.blank}{' '.join(items)}\n"
        match_010 += f'**{data["kills"]} / {data["deaths"]} / {data["assists"]}{Emoji.blank}{data["cs"]}{Emoji.history["cs"]}{Emoji.blank}{data["gold"]}{Emoji.history["gold"]}**'
        match_010 += f'\n{Emoji.blank}'

        embed.add_field(name=f'{emoji_map} {win}', value=match_100, inline=True)
        embed.add_field(name=Emoji.blank, value=match_010, inline=True)
        embed.add_field(name=Emoji.blank, value=match_001, inline=True)

        self.embed_history_light = embed
        return embed

    def match_embed(self, match):
        """ match embed """
        if match[1]['win']:
            win = 'VICTORY'
            embed_color = Color.victory
            if match[0]['gameMap'] == 'Howling Abyss': icon_map = Icon.ha_victory
            else: icon_map = Icon.sr_victory
        else:
            win = 'DEFEAT'
            embed_color = Color.defeat
            if match[0]['gameMap'] == 'Howling Abyss': icon_map = Icon.ha_defeat
            else: icon_map = Icon.sr_defeat
        
        title = f'{match[0]["gameMap"]} \u200b • \u200b {match[0]["gameDescription"]} \u200b • \u200b {match[0]["gameDuration"]} \u200b • \u200b <t:{match[0]["gameEndTimestamp"]}:d>'
        embed = discord.Embed(title=title, description='', color=embed_color)
        embed.set_author(name=f'{win}', icon_url=icon_map)

        team1_kda = f'**TEAM \u200b 1{Emoji.blank}\u200b {match[4]["kills"]} \u200b / \u200b {match[4]["deaths"]} \u200b / \u200b {match[4]["assists"]} \u200b {Emoji.history["kda"]}{Emoji.blank}**'
        team1_gold = f'{Emoji.blank}{Emoji.blank}{match[4]["gold"]} \u200b {Emoji.history["gold"]}'
        team1_icon_kda = f'{Emoji.blank}{Emoji.blank}{Emoji.blank}{Emoji.history["kda"]}'
        team1_champ = team1_item = team1_inv_kda = f''
        for player in match[2]:
            if len(player['position']) == 0: position = Emoji.position['FILL']
            try: position = Emoji.position[player['position']]
            except: position = Emoji.position['FILL']
            if match[0]['gameMap'] == 'Howling Abyss': position = ''
            if player['name'] == match[1]['name']: name = f'__*{player["name"]}*__'
            else: name = player['name']
            try: emoji_rune = Emoji.rune[player['rune']]
            except: emoji_rune = Emoji.rune['Runes']
            items = [Item.get_emoji(player["items"][i]) for i in range(7)]
            team1_item += f"{' '.join(items)}\n"
            team1_champ += f'{position}{emoji_rune} **{player["level"]}** \u200b {Emoji.champion[player["champion"]]} \u200b {name}\n'
            team1_inv_kda += f'{Emoji.blank} \u200b  \u200b **{player["kills"]} \u200b / \u200b {player["deaths"]} \u200b / \u200b {player["assists"]}**\n'
            
        embed.add_field(name=team1_kda, value=team1_champ, inline=True)
        embed.add_field(name=team1_gold, value=team1_item, inline=True)
        embed.add_field(name=team1_icon_kda, value=team1_inv_kda, inline=True)

        if len(match[6]) > 0: team1_title = 'BANS \u200b + \u200b OBJECTIVES'
        else: team1_title = 'OBJECTIVES'
        team1_ban = f''
        try:
            for i in range(5): team1_ban += f'{Emoji.champion[match[6][i]]}{Emoji.blank}'
        except: pass
        team1_obj = f'\n{Emoji.history["tower"]} \u200b {match[8][0]}{Emoji.blank}{Emoji.history["inhibitor"]} \u200b {match[8][1]}'
        if match[0]['gameMap'] == 'Summoner\'s Rift':
            team1_obj += f'{Emoji.blank}{Emoji.history["baron"]} \u200b {match[8][2]}{Emoji.blank}{Emoji.history["dragon"]} \u200b {match[8][3]}{Emoji.blank}{Emoji.history["herald"]} \u200b {match[8][4]}'
        team1_obj += f'\n{Emoji.blank}'

        embed.add_field(name=team1_title, value=team1_ban+team1_obj, inline=False)

        team2_kda = f'**TEAM \u200b 2{Emoji.blank}\u200b {match[5]["kills"]} \u200b / \u200b {match[5]["deaths"]} \u200b / \u200b {match[5]["assists"]} \u200b \u200b {Emoji.history["kda"]}{Emoji.blank}**'
        team2_gold = f'{Emoji.blank}{Emoji.blank}{match[5]["gold"]} \u200b {Emoji.history["gold"]}'
        team2_icon_kda = f'{Emoji.blank}{Emoji.blank}{Emoji.blank}{Emoji.history["kda"]}'
        team2_champ = team2_item = team2_inv_kda = f''
        for player in match[3]:
            if len(player['position']) == 0: position = Emoji.position['FILL']
            try: position = Emoji.position[player['position']]
            except: position = Emoji.position['FILL']
            if match[0]['gameMap'] == 'Howling Abyss': position = ''
            name = player['name']
            try: emoji_rune = Emoji.rune[player['rune']]
            except: emoji_rune = Emoji.rune['Runes']
            items = [Item.get_emoji(player["items"][i]) for i in range(7)]
            team2_item += f"{' '.join(items)}\n"
            team2_champ += f'{position}{emoji_rune} **{player["level"]}** \u200b {Emoji.champion[player["champion"]]} \u200b {name}\n'
            team2_inv_kda += f'{Emoji.blank} \u200b  \u200b **{player["kills"]} \u200b / \u200b {player["deaths"]} \u200b / \u200b {player["assists"]}**\n'
            
        embed.add_field(name=team2_kda, value=team2_champ, inline=True)
        embed.add_field(name=team2_gold, value=team2_item, inline=True)
        embed.add_field(name=team2_icon_kda, value=team2_inv_kda, inline=True)

        if len(match[7]) > 0: team2_title = 'BANS \u200b + \u200b OBJECTIVES'
        else: team2_title = 'OBJECTIVES'
        team2_ban = f''
        try:
            for i in range(5): team2_ban += f'{Emoji.champion[match[7][i]]}{Emoji.blank}'
        except: pass
        team2_obj = f'\n{Emoji.history["tower"]} \u200b {match[9][0]}{Emoji.blank}{Emoji.history["inhibitor"]} \u200b {match[9][1]}'
        if match[0]['gameMap'] == 'Summoner\'s Rift':
            team2_obj += f'{Emoji.blank}{Emoji.history["baron"]} \u200b {match[9][2]}{Emoji.blank}{Emoji.history["dragon"]} \u200b {match[9][3]}{Emoji.blank}{Emoji.history["herald"]} \u200b {match[9][4]}'
        team2_obj += f'\n{Emoji.blank}'

        embed.add_field(name=team2_title, value=team2_ban+team2_obj, inline=False)

        return embed

    def success(self, msg, desc):
        """ Embed for success command """
        embed = discord.Embed(
            title=f"```{msg}```",
            description=f"**{desc}**",
            color=Color.default,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f'COMMAND SUCCESS', icon_url=Icon.error)
        embed.set_thumbnail(url=Icon.poro_mission)
        return embed

    def region(self, new_region):
        """ Embed for region command """
        region = new_region.get('region')
        embed = discord.Embed(
            title=f"```{region.value[1]} ({region.value[0]})```",
            description=f"**Selected as default region.**",
            color=Color.default,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f'COMMAND SUCCESS', icon_url=Icon.error)
        # embed.set_thumbnail(url=Icon.transfer[region.value[0]])
        return embed

    def error(self, msg):
        """ Embed for command error """
        description = "Something went horribly wrong executing that command, please try again in a bit. If this error keeps happening, please send a bug report.\n\nTry '/help' for more information."
        embed = discord.Embed(
            title=f'```{msg}```',
            description=description,
            color=Color.error,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f'COMMAND ERROR', icon_url=Icon.error)
        embed.set_image(url=Icon.error_image)
        return embed

    def error_match(self, msg, description):
        """ Embed for match command error """
        embed = discord.Embed(
            title=f'{msg}',
            description=f'**{description}**',
            color=Color.error,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f'COMMAND ERROR', icon_url=Icon.error)
        embed.set_thumbnail(url=Icon.poro_error)
        return embed

    def system(self, msg, description):
        """ Embed for system command """
        embed = discord.Embed(
            title=f"```{msg}```",
            description=f"**{description}**",
            color=Color.error,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f'COMMAND ERROR', icon_url=Icon.error)
        embed.set_thumbnail(url=Icon.poro_error)
        return embed

    def setting(self, region, players, max):
        """ Embed for setting command """
        embed = discord.Embed(
            title="Selected data will be the default value for profile, player to update.",
            description="",
            color=Color.default,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f'SETTINGS', icon_url=Icon.setting)
        embed.add_field(
            name="REGION",
            value=f"```{region.value[0]} ({region.value[1]})```",
            inline=False
        )
        value_player = ""
        if len(players) == 0:
            value_player = "``` ```"

        for player in players:
            name = player.get('summoner').get('name')
            region = player.get('region')
            league = player.get('league')
            division = f"{league.get('tier')} {league.get('rank')}"
            lp = league.get('leaguePoints')
            wins = league.get('wins')
            losses = league.get('losses')
            try:
                value_player += f"```{name} #{region}\n{division} • {lp} LP | Win Rate {percent(wins, losses)}% • [{wins}W / {losses}L]```"
            except Exception as error:
                value_player += f"```{name} #{region}\nUnranked```"

        embed.add_field(
            name=f"PLAYER (Max. {max})",
            value=f"{value_player}",
            inline=False
        )
        return embed

    def help(self):
        """ List of commands """
        embed = discord.Embed(
            title="List of commands",
            description="",
            color=Color.default,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f'HELP', icon_url=Icon.book)
        embed.set_thumbnail(url=Icon.poro_voice)
        embed.add_field(
            name="help",
            value="```List of commands```",
            inline=False
        )
        embed.add_field(
            name="profile",
            value="```View selected summoner profile```",
            inline=False
        )
        embed.add_field(
            name="set-region",
            value="```Set the server's region```",
            inline=False
        )
        embed.add_field(
            name="setting",
            value="```View setting```",
            inline=False
        )
        embed.add_field(
            name="add-player",
            value="```Add player to the Update list```",
            inline=False
        )
        embed.add_field(
            name="delete-player",
            value="```Delete player from the Update list```",
            inline=False
        )
        return embed



class MyViewProfile(discord.ui.View):
    """ View for the bot """

    def __init__(self):
        super().__init__(timeout=None)
        self.embed_profile = None
        self.embed_history = None
        self.embed_match = None
        self.match = None

    def init_data(self, profile, history, match, match_data):
        self.embed_profile = profile
        self.embed_history = history
        self.embed_match = match
        self.match = match_data

    @discord.ui.button(label='OVERVIEW', style=discord.ButtonStyle.grey, custom_id='overview')
    async def overview(self, interaction: discord.Interaction, button: discord.ui.Button):
        for x in self.children:
            x.disabled = False
            if x.custom_id == 'match_select': 
                x.disabled = True
                for y in x.options: y.default = False

        button.disabled = True
        await interaction.response.edit_message(view=self, embed=self.embed_profile)

    @discord.ui.button(label='CHALLENGES', style=discord.ButtonStyle.grey, custom_id='challenges')
    async def challenges(self, interaction: discord.Interaction, button: discord.ui.Button):
        for x in self.children: 
            x.disabled = False
            if x.custom_id == 'match_select':
                x.disabled = True
                for y in x.options: y.default = False

        button.disabled = True
        await interaction.response.edit_message(view=self, content='In development...')

    @discord.ui.button(label='MATCH HISTORY', style=discord.ButtonStyle.grey , custom_id='match_history')
    async def history(self, interaction: discord.Interaction, button: discord.ui.Button):
        for x in self.children:
            x.disabled = False
            if x.custom_id == 'match_select':
                try: x.options = self.embed_match
                except: pass
                for y in x.options: y.default = False

        button.disabled = True
        await interaction.response.edit_message(view=self, embed=self.embed_history)

    @discord.ui.button(label='DEBUG', style=discord.ButtonStyle.red, custom_id='debug')
    async def debug(self, interaction: discord.Interaction, button: discord.ui.Button):
        for x in self.children:
            if x.custom_id != 'match_select': x.disabled = False
        await interaction.response.edit_message(view=self, content=f'```{Item.__undef__}```')

    @discord.ui.select(
        placeholder='MATCH DETAILS',
        options=[
            discord.SelectOption(label='Match 1', value='1'),
            discord.SelectOption(label='Match 2', value='2'),
            discord.SelectOption(label='Match 3', value='3'),
            discord.SelectOption(label='Match 4', value='4'),
            discord.SelectOption(label='Match 5', value='5')
        ],
        disabled=True,
        custom_id='match_select'
    )
    async def history_select(self, interaction=discord.Interaction, select=discord.ui.Select):
        for x in self.children: x.disabled = False
        for x in select.options: x.default = False
        select.options[int(select.values[0])-1].default = True
        embed = MyEmbed().match_embed(self.match[int(select.values[0])-1])
        await interaction.response.edit_message(view=self, embed=embed)


class MyViewUpdateMatch(discord.ui.View):
    """ View for the bot """

    def __init__(self, match, player):
        super().__init__(timeout=None)
        self.match_update = match
        self.player_update = player

    @discord.ui.button(label='MATCH DETAILS', style=discord.ButtonStyle.grey, custom_id='details')
    async def details(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MyViewUpdateBack(self.match_update, self.player_update)
        embed = MyEmbed().match_embed(self.match_update)
        await interaction.response.edit_message(view=view, embed=embed)

class MyViewUpdateBack(discord.ui.View):
    """ View for the bot """

    def __init__(self, match, player):
        super().__init__(timeout=None)
        self.match_update = match
        self.player_update = player

    @discord.ui.button(label='RETURN', style=discord.ButtonStyle.grey, custom_id='return')
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MyViewUpdateMatch(self.match_update, self.player_update)
        embed = MyEmbed().history_light_embed(self.match_update, self.player_update)
        await interaction.response.edit_message(view=view, embed=embed)