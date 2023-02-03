import discord
import json
import requests
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv
load_dotenv()

# Data & Resources
from data import Region, Platform, ddragon, Champion, Challenges, Summoner
from resources import Emoji, Icon

# Riot
from riotwatcher import LolWatcher, ApiError

riot_api_key = os.getenv('API_RIOT')
watcher = LolWatcher(riot_api_key)

# Global Variables
region = Region.europe_west.platform.value
summoner = None                 # 0: Id, 1: puuid, 2: name, 3: profileIcon, 4: level
ranks = None                    # 0: Solo, 1: Flex
masteryScore = None
masteries = None
challenges = None
matchList = None
history = None
match = None
match_select = None


MATCH_COUNT = 5
error_msg = {
'001a':"\nWE DIDN'T FIND ANY MATCHES FOR THIS PLAYER.\nTHIS MIGHT BE BECAUSE...",
'001b':f"{Emoji.blank}• This summoner hasn't played any ranked matches\n{Emoji.blank}• This summoner isn't fiends with the bot (and thus bot can't see{Emoji.blank} \u200b  \u200b their matches)\n{Emoji.blank}• This summoner hasn't played any matches since May 1st",
}


def resetGlobal():
    """ reset global variables """
    global summoner, ranks, masteryScore, masteries, challenges, matchList, history, match, authorName, authorIcon
    summoner = None
    ranks = None
    masteryScore = None
    masteries = None
    challenges = None
    matchList = None
    history = None
    match = None
    authorName = None
    authorIcon = None
    match_select = None

def set_region(new_region: str):
    """ set the region for the API """
    global region
    region = Region.from_platform(new_region).value
    msg = f"{Region.from_platform(new_region).region.value[1]} ({Region.from_platform(new_region).region.value[0]})"
    desc = "Selected as default region."
    platform = Region.from_platform(new_region).region.value[0]
    return (msg, desc, platform)

def set_summoner(data):
    global summoner
    summoner = data

def get_region(): return Platform.from_region(region).value[0]
def get_summoner(): return summoner
def get_ranks(): return ranks
def get_masteryScore(): return masteryScore
def get_masteries(): return masteries
def get_challenges(): return challenges
def get_matchList(): return matchList
def get_history(): return history
def get_match(): return match
def get_match_select(): return match_select


def fetchSummonerName(name: str):
    """ fetch a summoner by name """
    try:
        summoner = watcher.summoner.by_name(region, name)

        id = summoner['id']
        puuid = summoner['puuid']
        name = summoner['name']
        profileIcon = ddragon.url_profileicon + str(summoner['profileIconId']) + '.png'
        level = 'Lvl. ' + str(summoner['summonerLevel'])

        return (id, puuid, name, profileIcon, level)
    except ApiError as error:
        if error.response.status_code == 404:
            return f"'{name}': Summoner not found"
        elif error.response.status_code == 429:
            return 'Riot Games API key rate limit reached'
        elif error.response.status_code == 403:
            return 'Riot Games API key expired'
        else: raise

def fetchSummonerPuuid(puuid: str):
    """ fetch a summoner by name """
    try:
        summoner = watcher.summoner.by_puuid(region, puuid)

        id = summoner['id']
        puuid = summoner['puuid']
        name = summoner['name']
        profileIcon = ddragon.url_profileicon + str(summoner['profileIconId']) + '.png'
        level = 'Lvl. ' + str(summoner['summonerLevel'])

        return (id, puuid, name, profileIcon, level)
    except ApiError as error:
        if error.response.status_code == 404:
            return f"'{name}': Summoner not found"
        elif error.response.status_code == 429:
            return 'Riot Games API key rate limit reached'
        elif error.response.status_code == 403:
            return 'Riot Games API key expired'
        else: raise

def fetchSummonerRegion(name: str, _region: str):
    """ fetch a summoner by name """
    try:
        summoner = watcher.summoner.by_name(_region, name)

        id = summoner['id']
        puuid = summoner['puuid']
        name = summoner['name']
        profileIcon = ddragon.url_profileicon + str(summoner['profileIconId']) + '.png'
        level = 'Lvl. ' + str(summoner['summonerLevel'])

        return (id, puuid, name, profileIcon, level)
    except ApiError as error:
        if error.response.status_code == 404:
            return f"'{name}': Summoner not found"
        elif error.response.status_code == 429:
            return 'Riot Games API key rate limit reached'
        elif error.response.status_code == 403:
            return 'Riot Games API key expired'
        else: raise

def fetchRanks(encryptedSummonerId: str):
    """ fetch the ranks of a summoner """
    try:
        ranks = watcher.league.by_summoner(region, encryptedSummonerId)

        calls = {0:'queueType', 1:'tier', 2:'rank', 3:'leaguePoints', 4:'wins', 5:'losses'}
        solo = [None, None, None, None, None, None]
        flex = [None, None, None, None, None, None]
        try:
            for i in range(0, 2):
                for j in range(0, len(calls)):
                    if ranks[i][calls[0]] == 'RANKED_SOLO_5x5':
                        solo[j] = ranks[i][calls[j]]
                    if ranks[i][calls[0]] == 'RANKED_FLEX_SR':
                        flex[j] = ranks[i][calls[j]]
        except: pass

        return (solo, flex)
    except ApiError as error:
        if error.response.status_code == 404:
            return f"'{encryptedSummonerId}': Summoner not found"
        elif error.response.status_code == 429:
            return 'Riot Games API key rate limit reached'
        elif error.response.status_code == 403:
            return 'Riot Games API key expired'
        else: raise

def fetchMasteryScore(encryptedSummonerId: str):
    """ fetch the mastery score of a summoner """
    try:
        return watcher.champion_mastery.scores_by_summoner(region, encryptedSummonerId)
    except ApiError as error:
        if error.response.status_code == 404:
            return f"'{encryptedSummonerId}': Summoner not found"
        elif error.response.status_code == 429:
            return 'Riot Games API key rate limit reached'
        elif error.response.status_code == 403:
            return 'Riot Games API key expired'
        else: raise

def fetchMasteries(encryptedSummonerId: str):
    """ fetch the masteries of a summoner """
    try:
        masteries = watcher.champion_mastery.by_summoner(region, encryptedSummonerId)[:3]

        ids, levels, points, names = [], [], [], []
        for champion in masteries:
            ids.append(champion['championId'])
            levels.append('Level_'+str(champion['championLevel']))
            tmp = str(champion['championPoints'])
            tmp = '{:,}'.format(int(tmp))
            points.append(tmp)

        for id in ids: names.append(Champion.from_id(id))

        return (names, levels, points)
    except ApiError as error:
        if error.response.status_code == 404:
            return f"'{encryptedSummonerId}': Summoner not found"
        elif error.response.status_code == 429:
            return 'Riot Games API key rate limit reached'
        elif error.response.status_code == 403:
            return 'Riot Games API key expired'
        else: raise

def fetchChallenges(puuid: str):
    """ fetch the challenges of a summoner """
    try:
        challenges = watcher.challenges.by_puuid(region, puuid)

        try:
            id = challenges['preferences']['title']
            if len(id) == 0: return None
        except: return None

        title = Challenges.from_id(id)

        return (title, True)
    except ApiError as error:
        if error.response.status_code == 404:
            return f"'{puuid}': Summoner not found"
        elif error.response.status_code == 429:
            return 'Riot Games API key rate limit reached'
        elif error.response.status_code == 403:
            return 'Riot Games API key expired'
        else: raise

def fetchMatchList(puuid: str, count: int):
    """ fetch the match list of a summoner """
    try:
        return watcher.match.matchlist_by_puuid(region, puuid, 0, count)
    except ApiError as error:
        if error.response.status_code == 404:
            return f"'{puuid}': Summoner not found"
        elif error.response.status_code == 429:
            return 'Riot Games API key rate limit reached'
        elif error.response.status_code == 403:
            return 'Riot Games API key expired'
        else: raise

def fetchMatch(matchId: str, puuid: str):
    """ fetch the match of matchId """
    try:
        match = watcher.match.by_id(region, matchId)

        gameMode = match['info']['gameMode']
        queueId = match['info']['queueId']

        gameID = match['metadata']['matchId']
        # clear game Id 
        index = gameID.find('_') + 1
        if index != -1: gameID = gameID[index:]

        gameEnd = match['info']['gameEndTimestamp']
        gameEndTimestamp = round(gameEnd/1000)
        # adjust time
        date_tmp = datetime.fromtimestamp(gameEnd/1000).strftime('%d/%m/%Y')
        gameEnd = date_tmp

        gameDuration = match['info']['gameDuration']
        # clear game duration
        delta_tmp = timedelta(seconds=gameDuration)
        delta_tmp = str(delta_tmp).split(':')
        if delta_tmp[0] == '0': gameDuration = delta_tmp[1] + ':' + delta_tmp[2]
        else: gameDuration = delta_tmp[0] + ':' + delta_tmp[1] + ':' + delta_tmp[2]

        try:
            queues_db = requests.get(ddragon.url_queues).json()
            for queue in queues_db:
                if queue['queueId'] == queueId:
                    gameMap = queue['map']
                    gameDescription = queue['description']
                    break

            # clear game description
            gameDescription = gameDescription.replace(' games', '')
            gameDescription = gameDescription.replace('5v5 ', '')
            gameDescription = gameDescription.replace('3v3 ', '')
            gameDescription = gameDescription.replace('Solo', 'Solo/Duo')
            gameDescription = gameDescription.replace('Pick URF', 'Ultra Rapid Fire')
            gameDescription = gameDescription.replace('Draft Pick', 'Normal (Draft Pick)')
            gameDescription = gameDescription.replace('Co-op vs. AI', '')
            gameDescription = gameDescription.replace('Bot', '')
        except Exception: return 'Fail requests ddragon queues'

        gameInfo = {
            'gameEndTimestamp': gameEndTimestamp,
            'gameEnd': gameEnd,
            'gameDuration': gameDuration,
            'gameMap': gameMap,
            'gameDescription': gameDescription,
            'gameID': gameID
        }

        # print(match['metadata']['matchId'])

        team1, team2, team_tmp = [], [], []
        for participant in match['info']['participants']:
            position = participant['teamPosition']
            if (gameMode == 'ARAM'): position = 'MIDDLE'
            player = {
                'name': participant['summonerName'],
                'champion': Champion.fix_name(participant['championName']),
                'level': participant['champLevel'],
                'kills': participant['kills'],
                'deaths': participant['deaths'],
                'assists': participant['assists'],
                'gold': participant['goldEarned'],
                'cs': participant['totalMinionsKilled'] + participant['neutralMinionsKilled'],
                'items': [participant['item0'], participant['item1'], participant['item2'], participant['item3'], participant['item4'], participant['item5'], participant['item6']],
                'summonerSpells1': participant['summoner1Id'], 
                'summonerSpells2': participant['summoner2Id'],
                'rune': participant['perks']['styles'][0]['selections'][0]['perk'],
                'position': position,
                'win': participant['win'],
                'kda': None,
                'kp': None,
            }
            if participant['win']:
                if participant['puuid'] == puuid:
                    team_tmp.append(player)
                    team_tmp.append(False)
                team1.append(player)
            else:
                if participant['puuid'] == puuid:
                    team_tmp.append(player)
                    team_tmp.append(True)
                team2.append(player)

        if team_tmp[1]:
            tmp = team1
            team1 = team2
            team2 = tmp

        total_kills1 = total_deaths1 = total_assists1 = total_gold1 = 0
        total_kills2 = total_deaths2 = total_assists2 = total_gold2 = 0
        for i in range(5):
            total_kills1 += team1[i]['kills']
            total_deaths1 += team1[i]['deaths']
            total_assists1 += team1[i]['assists']
            total_gold1 += team1[i]['gold']
            total_kills2 += team2[i]['kills']
            total_deaths2 += team2[i]['deaths']
            total_assists2 += team2[i]['assists']
            total_gold2 += team2[i]['gold']

        total_gold1 = '{:,}'.format(total_gold1)
        total_gold2 = '{:,}'.format(total_gold2)

        try: runes_db = requests.get(ddragon.url_runesReforged).json()
        except Exception: return 'Fail requests ddragon runes reforged'

        for i in range(5):
            try:
                team1[i]['kda'] = f"{round((team1[i]['kills'] + team1[i]['assists']) / team1[i]['deaths'], 1)}"
                team2[i]['kda'] = f"{round((team2[i]['kills'] + team2[i]['assists']) / team2[i]['deaths'], 1)}"
            except ZeroDivisionError:
                team1[i]['kda'] = f"{round((team1[i]['kills'] + team1[i]['assists']), 1)}"
                team2[i]['kda'] = f"{round((team2[i]['kills'] + team2[i]['assists']), 1)}"
            try:
                team1[i]['kp'] = f"{round((team1[i]['kills'] + team1[i]['assists']) / total_kills1 * 100)}%"
                team2[i]['kp'] = f"{round((team2[i]['kills'] + team2[i]['assists']) / total_kills2 * 100)}%"
            except ZeroDivisionError:
                team1[i]['kp'] = f"100%"
                team2[i]['kp'] = f"100%"
            team1[i]['gold'] = '{:,}'.format(team1[i]['gold'])
            team2[i]['gold'] = '{:,}'.format(team2[i]['gold'])
            team1[i]['summonerSpells1'] = Summoner.from_key(team1[i]['summonerSpells1']).value
            team1[i]['summonerSpells2'] = Summoner.from_key(team1[i]['summonerSpells2']).value
            team2[i]['summonerSpells1'] = Summoner.from_key(team2[i]['summonerSpells1']).value
            team2[i]['summonerSpells2'] = Summoner.from_key(team2[i]['summonerSpells2']).value
            for rune in runes_db:
                for slot in rune['slots']:
                    for rune in slot['runes']:
                        if rune['id'] == team1[i]['rune']: team1[i]['rune'] = rune['name']
                        if rune['id'] == team2[i]['rune']: team2[i]['rune'] = rune['name']
        
        total_team1 = {
            'win': team1[0]['win'],
            'kills': total_kills1,
            'deaths': total_deaths1,
            'assists': total_assists1,
            'gold': total_gold1,
        }
        total_team2 = {
            'win': team2[0]['win'],
            'kills': total_kills2,
            'deaths': total_deaths2,
            'assists': total_assists2,
            'gold': total_gold2,
        }

        if team1[0]['win']:
            if match['info']['teams'][0]['win']: teamCase = True
            else: teamCase = False
        else:
            if match['info']['teams'][0]['win']: teamCase = False
            else: teamCase = True

        if teamCase:
            tmp_bans1 = match['info']['teams'][0]['bans']
            tmp_objectives1 = match['info']['teams'][0]['objectives']
            tmp_bans2 = match['info']['teams'][1]['bans']
            tmp_objectives2 = match['info']['teams'][1]['objectives']
        else:
            tmp_bans1 = match['info']['teams'][1]['bans']
            tmp_objectives1 = match['info']['teams'][1]['objectives']
            tmp_bans2 = match['info']['teams'][0]['bans']
            tmp_objectives2 = match['info']['teams'][0]['objectives']

        team1_bans, team2_bans = [], []
        try:
            try: champions_db = requests.get(ddragon.url_champion).json()
            except Exception: return 'Fail requests ddragon champion'
            for i in range(5):
                if int(tmp_bans1[i]['championId']) == -1: team1_bans.append('None')
                if int(tmp_bans2[i]['championId']) == -1: team2_bans.append('None')
                for champion in champions_db['data']:
                    if int(champions_db['data'][champion]['key']) == int(tmp_bans1[i]['championId']):
                        team1_bans.append(champions_db['data'][champion]['name'])
                    if int(champions_db['data'][champion]['key']) == int(tmp_bans2[i]['championId']):
                        team2_bans.append(champions_db['data'][champion]['name'])
        except: pass

        team1_objectives, team2_objectives = [], []
        calls = {0:'tower', 1:'inhibitor', 2:'baron', 3:'dragon', 4:'riftHerald'}
        for i in range(5):
            if tmp_objectives1[calls[i]]: 
                team1_objectives.append(tmp_objectives1[calls[i]]['kills'])
            if tmp_objectives2[calls[i]]: 
                team2_objectives.append(tmp_objectives2[calls[i]]['kills'])

        return (gameInfo, team_tmp[0], team1, team2, total_team1, total_team2, team1_bans, team2_bans, team1_objectives, team2_objectives)

    except ApiError as error:
        if error.response.status_code == 404:
            return f"'{matchId}': Match not found"
        elif error.response.status_code == 429:
            return 'Riot Games API key rate limit reached'
        elif error.response.status_code == 403:
            return 'Riot Games API key expired'
        else: raise





# """ 
#  # Get summoner match history from Riot API
#  #
#  # Parameters defined in global variables
#  # @param region: The region of the summoner
#  # @param summonerId: The summoner ID of the summoner
#  #
#  # Only returns 5 last matches
#  # Total 6 requests to Riot API
#  """

def requestProfile():
    """ request the profile of a summoner """
    if summoner == None: return 'Summoner not found'

    # Summoner Rank
    _rank = fetchRanks(summoner[0])
    if isinstance(_rank, str): return _rank

    # Summoner Mastery Score
    _score = fetchMasteryScore(summoner[0])
    if isinstance(_score, str): return _score

    # Summoner Masteries
    _masteries = fetchMasteries(summoner[0])
    if isinstance(_masteries, str): return _masteries

    # Summoner Challenges
    _challenges = fetchChallenges(summoner[1])
    if isinstance(_challenges, str): return _challenges

    # Set global variables
    global ranks, masteryScore, masteries, challenges
    ranks = _rank
    masteryScore = _score
    masteries = _masteries
    challenges = _challenges


def requestMatchHistory():
    """ request match history of a summoner """
    if summoner == None: return 'Summoner Name missing'

    # Summoner History List
    matchId = fetchMatchList(summoner[1], MATCH_COUNT)
    if isinstance(matchId, str): return matchId

    # Summoner Match History
    allHistory = []
    try:
        for i in range(0, len(matchId)):
            matchHistory = fetchMatch(matchId[i], summoner[1])
            if isinstance(matchHistory, str): return matchHistory

            allHistory.append(matchHistory)
    except Exception as error:
        item_undefined.append(error)
        return (error_msg['001a'], error_msg['001b'])

    # Slice History
    match1, match2, match3, match4, match5 = [], [], [], [], []
    match1.append(allHistory[0][0])
    match1.append(allHistory[0][1])
    match2.append(allHistory[1][0])
    match2.append(allHistory[1][1])
    match3.append(allHistory[2][0])
    match3.append(allHistory[2][1])
    match4.append(allHistory[3][0])
    match4.append(allHistory[3][1])
    match5.append(allHistory[4][0])
    match5.append(allHistory[4][1])
    allMinHistory = [match1, match2, match3, match4, match5]

    # Set global variables
    global matchList, history, match
    matchList = matchId
    history = allMinHistory
    match = allHistory

    # Embed List of Match
    match_label = []
    match_emoji = []
    match_description = []
    for i in range(0, 5):
        if allMinHistory[i][1]['win']:
            title = 'VICTORY'
            if allMinHistory[i][0]['gameMap'] == 'Howling Abyss': match_emoji.append(Emoji.aram['victory'])
            else: match_emoji.append(Emoji.sr['victory'])
        else:
            title = 'DEFEAT \u200b  \u200b  \u200b '
            if allMinHistory[i][0]['gameMap'] == 'Howling Abyss': match_emoji.append(Emoji.aram['defeat'])
            else: match_emoji.append(Emoji.sr['defeat'])

        name = Champion.fix_name(allMinHistory[i][1]['champion'])
        match_label.append(f'{title} \u200b | \u200b {name} \u200b  \u200b  \u200b  \u200b {allMinHistory[i][1]["kills"]} \u200b / \u200b {allMinHistory[i][1]["deaths"]} \u200b / \u200b {allMinHistory[i][1]["assists"]}')
        match_description.append(f'{allMinHistory[i][0]["gameDescription"]} \u200b • \u200b {allMinHistory[i][0]["gameDuration"]} \u200b • \u200b {allMinHistory[i][0]["gameEnd"]}')

    global match_select
    match_select = [
            discord.SelectOption(label=match_label[0], description=match_description[0], emoji=match_emoji[0], value='1'),
            discord.SelectOption(label=match_label[1], description=match_description[1], emoji=match_emoji[1], value='2'),
            discord.SelectOption(label=match_label[2], description=match_description[2], emoji=match_emoji[2], value='3'),
            discord.SelectOption(label=match_label[3], description=match_description[3], emoji=match_emoji[3], value='4'),
            discord.SelectOption(label=match_label[4], description=match_description[4], emoji=match_emoji[4], value='5')
        ]


def strAdd(str):
    if "0/10" in str: return str.replace("0/10", "1/10")
    if "1/10" in str: return str.replace("1/10", "2/10")
    if "2/10" in str: return str.replace("2/10", "3/10")
    if "3/10" in str: return str.replace("3/10", "4/10")
    if "4/10" in str: return str.replace("4/10", "5/10")
    if "5/10" in str: return str.replace("5/10", "6/10")
    if "6/10" in str: return str.replace("6/10", "7/10")
    if "7/10" in str: return str.replace("7/10", "8/10")
    if "8/10" in str: return str.replace("8/10", "9/10")
    if "9/10" in str: return str.replace("9/10", "10/10")

def updateRank(player: list):
    try: matchId = fetchMatchList(player[3], 1)[0]
    except: return "Match not found"
    if matchId == player[5]: return "No new match"
    match = fetchMatch(matchId, player[3])
    if (match[0]['gameDescription'] != "Ranked Solo/Duo"): return "Not a ranked match"

    player[5] = matchId # Update match ID
    rank = fetchRanks(player[2])[0] # Get new rank
    rank.remove(rank[0])

    # Calculate LP change
    try:
        win = match[1]['win']

        try: last_lp = int(player[4][2])
        except: last_lp = 0
        try: current_lp = int(rank[2])
        except: current_lp = 0

        lp = abs(current_lp - last_lp)
        if win: lp = "+" + str(lp) + " LP"
        else: lp = "-" + str(lp) + " LP"

        if player[4][2] == 100 and rank[2] == 100: lp = "Promotion Series"

        if player[4][1] != rank[1] and win: lp = "PROMOTED TO " + str(rank[0]) + " " + str(rank[1])
        if player[4][1] != rank[1] and not win: lp = "DEMOTE TO " + str(rank[0]) + " " + str(rank[1])

        if player[4][0] != rank[0] and win: lp = "PROMOTED TO " + str(rank[0]) + " " + str(rank[1])
        if player[4][0] != rank[0] and not win: lp = "DEMOTE TO " + str(rank[0]) + " " + str(rank[1])

        if "PLACEMENTS" in player[7] and player[4][0] == "UNRANKED": lp = strAdd(player[7])
        if "PLACEMENTS 10/10" in player[7] and player[4][0] == "UNRANKED": lp = "PLACED INTO " + str(rank[0]) + " " + str(rank[1])
    except Exception as e: lp = "PLACEMENTS 0/10"

    player[7] = lp      # Update match result
    player[4] = rank    # Update rank

    # Update Summoner Name
    summoner = fetchSummonerPuuid(player[3])
    player[1] = summoner[2]

    return match
