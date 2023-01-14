import datetime
from datetime import datetime, timedelta

# Discord bot
import discord
from discord import Embed
from discord.ui import View, button, Select

# Resources
from resources import Emoji, Icon, Color


def replaceSpaces(string: str):
    """ replace spaces with underscores """
    return string.replace(' ', '%20')

def percent(wins: int, losses: int):
    """ calculate the winrate """
    return round((wins / (wins + losses)) * 100)

def spacing(rank: str, wins: int, losses: int):
    """ calculate the spacing between the rank and the winrate """
    if rank == 'IRON' or rank == 'GOLD': spaces = f'{Emoji.blank}{Emoji.blank}{Emoji.blank} \u200b \u200b '
    if rank == 'BRONZE' or rank == 'SILVER' or rank == 'MASTER': spaces = f'{Emoji.blank}{Emoji.blank}{Emoji.blank}'
    if rank == 'PLATINUM' or rank == 'DIAMOND': spaces = f'{Emoji.blank} \u200b \u200b \u200b \u200b '
    if rank == 'GRANDMASTER' or rank == 'CHALLENGER': return f'{Emoji.blank} \u200b '
    if wins > 99: spaces += '\u200b \u200b '
    if losses > 99: spaces += '\u200b \u200b '
    return spaces


authorName = None
authorIcon = None
region = None
summoner = None
ranks = None
masteryScore = None
masteries = None
challenges = None
history = None
match = None
match_select = None

class Data:

    def set_author(name, icon):
        global authorName, authorIcon
        authorName = name
        authorIcon = icon

    def update(_region, _summoner, _ranks, _masteryScore, _masteries, _challenges, _history, _match, _match_select):
        global region, summoner, ranks, masteryScore, masteries, challenges, history, match, match_select
        region = _region
        summoner = _summoner
        ranks = _ranks
        masteryScore = _masteryScore
        masteries = _masteries
        challenges = _challenges
        history = _history
        match = _match
        match_select = _match_select

class MyEmbed:
    """ Embed for the bot """

    def profile():
        """ profile embed """
        try: description = f'{summoner[4]} \u200b | \u200b {challenges[0]}'
        except: description = summoner[4]
        
        try: opgg = f'https://www.op.gg/summoners/{region}/{replaceSpaces(summoner[2])}'
        except: opgg = f'https://www.op.gg/'

        embed = discord.Embed(title=f'**{summoner[2]} \u200b #{region}**', url=opgg, description=description, color=Color.default, timestamp=datetime.utcnow())
        embed.set_thumbnail(url=summoner[3])
        embed.set_author(name=f'Summoner \u200b Profile \u200b \u200b • \u200b \u200b OVERVIEW', icon_url=Icon.nav_profile)
        embed.set_footer(text=authorName, icon_url=authorIcon)

        # Rank Solo/Duo & Flex
        value_solo = value_flex = f'{Emoji.tier["UNRANKED"]} \u200b **Unranked** \n{Emoji.blank}'

        if ranks[0][0] != None:
            spaces_solo = spacing(ranks[0][1], ranks[0][4], ranks[0][5])
            value_solo = f'{Emoji.tier[ranks[0][1]]} \u200b **{ranks[0][1]} {ranks[0][2]}**{spaces_solo}{ranks[0][3]} LP\n'
            value_solo += f'**Win Rate {percent(ranks[0][4], ranks[0][5])}%**{Emoji.blank}{ranks[0][4]}W / {ranks[0][5]}L\n{Emoji.blank}'
        if ranks[1][0] != None:
            spaces_flex = spacing(ranks[0][1], ranks[0][4], ranks[0][5])
            value_flex = f'{Emoji.tier[ranks[0][1]]} \u200b **{ranks[0][1]} {ranks[0][2]}**{spaces_flex}{ranks[0][3]} LP\n'
            value_flex += f'**Win Rate {percent(ranks[0][4],ranks[0][5])}%**{Emoji.blank}{ranks[0][4]}W / {ranks[0][5]}L\n{Emoji.blank}'

        embed.add_field(name='SOLO/DUO', value=value_solo, inline=True)
        embed.add_field(name='FLEX 5V5', value=value_flex, inline=True)

        # Mastery Score
        embed.add_field(name='MASTERY \u200b SCORE', value=f'{Emoji.mastery["default"]} \u200b **{masteryScore}**\n{Emoji.blank}', inline=False)

        # Champions Masteries
        champion_mastery_1 = f'{Emoji.mastery[masteries[1][0]]} \u200b {Emoji.champion[masteries[0][0]]} \u200b **{masteries[0][0].upper()}** \n'
        champion_mastery_1 += f'{Emoji.mastery["default"]} \u200b {masteries[2][0]} pts \n{Emoji.blank}'
        champion_mastery_2 = f'{Emoji.mastery[masteries[1][1]]} \u200b {Emoji.champion[masteries[0][1]]} \u200b **{masteries[0][1].upper()}** \n'
        champion_mastery_2 += f'{Emoji.mastery["default"]} \u200b {masteries[2][1]} pts \n{Emoji.blank}'
        champion_mastery_3 = f'{Emoji.mastery[masteries[1][2]]} \u200b {Emoji.champion[masteries[0][2]]} \u200b **{masteries[0][2].upper()}** \n'
        champion_mastery_3 += f'{Emoji.mastery["default"]} \u200b {masteries[2][2]} pts \n{Emoji.blank}'

        embed.add_field(name='HIGHEST', value=champion_mastery_1, inline=True)
        embed.add_field(name='CHAMPION', value=champion_mastery_2, inline=True)
        embed.add_field(name='SCORE', value=champion_mastery_3, inline=True)

        return embed

    def history():
        """ history embed """
        embed = discord.Embed(title=f'RECENT \u200b GAMES \u200b (LAST 5 PLAYED)', description='', color=Color.default, timestamp=datetime.utcnow())
        embed.set_author(name=f'Summoner \u200b Profile \u200b \u200b • \u200b \u200b MATCH \u200b HISTORY', icon_url=Icon.nav_profile)
        embed.set_footer(text=authorName, icon_url=authorIcon)

        for i in range(0, len(history)):
            info = history[i][0]
            data = history[i][1]

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
            match_100 += f'{Emoji.blank}{Emoji.blank}{Emoji.blank}'
            match_001 = f'{info["gameMap"]}\n{info["gameDuration"]} \u200b  • \u200b <t:{info["gameEndTimestamp"]}:d>'
                
            try:
                item0 = Emoji.item[data["items"][0]]
                item1 = Emoji.item[data["items"][1]]
                item2 = Emoji.item[data["items"][2]]
                item3 = Emoji.item[data["items"][3]]
                item4 = Emoji.item[data["items"][4]]
                item5 = Emoji.item[data["items"][5]]
                item6 = Emoji.item[data["items"][6]]
            except: item0 = item1 = item2 = item3 = item4 = item5 = item6 = Emoji.item[0]

            match_010 = f'{Emoji.blank}{item0} \u200b {item1} \u200b {item2} \u200b {item3} \u200b {item4} \u200b {item5} \u200b {item6}\n'
            match_010 += f'**{data["kills"]} / {data["deaths"]} / {data["assists"]}{Emoji.blank}{data["cs"]} {Emoji.history["cs"]}{Emoji.blank}{data["gold"]} {Emoji.history["gold"]}**'

            embed.add_field(name=f'{emoji_map} {win}', value=match_100, inline=True)
            embed.add_field(name=Emoji.blank, value=match_010, inline=True)
            embed.add_field(name=Emoji.blank, value=match_001, inline=True)

        return embed

    def match(match):
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
        embed = discord.Embed(title=title, description='', color=embed_color, timestamp=datetime.utcnow())
        embed.set_author(name=f'{win}', icon_url=icon_map)
        embed.set_footer(text=authorName, icon_url=authorIcon)

        team1_kda = f'**TEAM \u200b 1{Emoji.blank}\u200b {match[4]["kills"]} \u200b / \u200b {match[4]["deaths"]} \u200b / \u200b {match[4]["assists"]} \u200b \u200b {Emoji.history["kda"]}{Emoji.blank}**'
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
            try: item0 = Emoji.item[player['items'][0]]
            except: 
                item0 = Emoji.item[0]
                item_undefined.append(player['items'][0])
            try: item1 = Emoji.item[player['items'][1]]
            except:
                item1 = Emoji.item[0]
                item_undefined.append(player['items'][1])
            try: item2 = Emoji.item[player['items'][2]]
            except:
                item2 = Emoji.item[0]
                item_undefined.append(player['items'][2])
            try: item3 = Emoji.item[player['items'][3]]
            except:
                item3 = Emoji.item[0]
                item_undefined.append(player['items'][3])
            try: item4 = Emoji.item[player['items'][4]]
            except: 
                item4 = Emoji.item[0]
                item_undefined.append(player['items'][4])
            try: item5 = Emoji.item[player['items'][5]]
            except: 
                item5 = Emoji.item[0]
                item_undefined.append(player['items'][5])
            try: item6 = Emoji.item[player['items'][6]]
            except: 
                item6 = Emoji.item[0]
                item_undefined.append(player['items'][6])
            team1_champ += f'{position}{emoji_rune} **{player["level"]}** \u200b {Emoji.champion[player["champion"]]} \u200b {name}\n'
            team1_item += f'{item0} {item1} {item2} {item3} {item4} {item5} {item6}\n'
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
            try: item0 = Emoji.item[player['items'][0]]
            except: 
                item0 = Emoji.item[0]
                item_undefined.append(player['items'][0])
            try: item1 = Emoji.item[player['items'][1]]
            except:
                item1 = Emoji.item[0]
                item_undefined.append(player['items'][1])
            try: item2 = Emoji.item[player['items'][2]]
            except:
                item2 = Emoji.item[0]
                item_undefined.append(player['items'][2])
            try: item3 = Emoji.item[player['items'][3]]
            except:
                item3 = Emoji.item[0]
                item_undefined.append(player['items'][3])
            try: item4 = Emoji.item[player['items'][4]]
            except: 
                item4 = Emoji.item[0]
                item_undefined.append(player['items'][4])
            try: item5 = Emoji.item[player['items'][5]]
            except: 
                item5 = Emoji.item[0]
                item_undefined.append(player['items'][5])
            try: item6 = Emoji.item[player['items'][6]]
            except: 
                item6 = Emoji.item[0]
                item_undefined.append(player['items'][6])
            team2_champ += f'{position}{emoji_rune} **{player["level"]}** \u200b {Emoji.champion[player["champion"]]} \u200b {name}\n'
            team2_item += f'{item0} {item1} {item2} {item3} {item4} {item5} {item6}\n'
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

        embed.add_field(name=team2_title, value=team2_ban+team2_obj, inline=False)

        return embed

    def success(msg):
        embed = discord.Embed(title=f'```{msg}```', description="", color=Color.success, timestamp=datetime.utcnow())
        embed.set_author(name=f'COMMAND SUCCESS', icon_url=Icon.error)
        embed.set_footer(text=authorName, icon_url=authorIcon)
        embed.set_thumbnail(url=Icon.poro_mission)
        return embed

    def error(msg):
        description = "Something went horribly wrong executing that command, please try again in a bit. If this error keeps happening, please send a bug report.\n\nTry '/help' for more information."
        embed = discord.Embed(title=f'```Error : {msg}```', description=description, color=Color.error, timestamp=datetime.utcnow())
        embed.set_author(name=f'COMMAND ERROR', icon_url=Icon.error)
        embed.set_footer(text=authorName, icon_url=authorIcon)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1039594104759271428/1063602226729340928/EMRATA_024a.jpg")
        return embed

    def system(msg, desc):
        embed = discord.Embed(title=msg, description=desc, color=Color.error, timestamp=datetime.utcnow())
        embed.set_author(name=f'COMMAND ERROR', icon_url=Icon.error)
        embed.set_footer(text=authorName, icon_url=authorIcon)
        # embed.set_image(url="https://www.instyle.com/thmb/FdMSR6RmfxSqrLvy9HVzzH_FE_c=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/103122-Emrata-Social-ade4acc948ea4bae952ed8636e94774b.jpg")
        return embed


# Data
from data import item_undefined

class MyView(discord.ui.View):
    """ View for the bot """

    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='OVERVIEW', style=discord.ButtonStyle.grey, custom_id='overview')
    async def overview(self, interaction: discord.Interaction, button: discord.ui.Button):
        for x in self.children:
            x.disabled = False
            if x.custom_id == 'match_select': 
                x.disabled = True
                for y in x.options: y.default = False

        button.disabled = True
        embed = MyEmbed.profile()
        await interaction.response.edit_message(view=self, embed=embed)

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
                try: x.options = match_select
                except: pass
                for y in x.options: y.default = False

        button.disabled = True
        embed = MyEmbed.history()
        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(label='DEBUG', style=discord.ButtonStyle.red, custom_id='debug')
    async def debug(self, interaction: discord.Interaction, button: discord.ui.Button):
        for x in self.children: x.disabled = False
        await interaction.response.edit_message(view=self, content=f'```{item_undefined}```')

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
        embed = MyEmbed.match(match[int(select.values[0])-1])
        await interaction.response.edit_message(view=self, embed=embed)