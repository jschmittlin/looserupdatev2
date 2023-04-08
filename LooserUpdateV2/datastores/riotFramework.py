import discord
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

from riotwatcher import LolWatcher, ApiError

from .ddragon import DDragon

from core.data import Region, Platform, Champion, Challenges, Summoner, Queue
from core.resources import Emoji
from core.common import str_digit_add

load_dotenv()
riot_api_key = os.getenv('API_RIOT')
watcher = LolWatcher(riot_api_key)

class RiotFramework(): 
    """ Riot Framework """

    def __init__(self):
        self.region = {
            'platform': Platform.europe_west,
            'region':   Region.europe_west,
        }
        self.summoner = {
            'id':               None,
            'puuid':            None,
            'name':             None,
            'profileIcon':      None,
            'level':            None,
        }
        self.league = {
            'solo': {
                'tier':         None,
                'rank':         None,
                'leaguePoints': None,
                'wins':         None,
                'losses':       None,
            },
            'flex': {
                'tier':         None,
                'rank':         None,
                'leaguePoints': None,
                'wins':         None,
                'losses':       None,
            },
        }
        self.mastery_score =    None
        self.masteries = {
            'championNames':    None,
            'championLevels':   None,
            'championPoints':   None,
        }
        self.challenges = {
            'title':            None,
        }
        self.match_list         = None
        self.history            = None
        self.match              = None
        self.match_select       = None
        self.match_max          = 5

    def reset(self):
        """ Resets all variables to their default values. """
        self.__init__()


    def set_region(self, region):
        """
        Sets the region.

        :param region: The new region to set.
        """
        platform = Region.from_platform(region)
        self.region = {
            'platform': platform,
            'region':   platform.region,
        }



    """ API Calls """
    def handle_api_error(error, description: str):
        """ 
        Handles API errors.

        :param error: The error to handle.
        :param description: The description of the error.

        :return: The error message.
        """
        status_code = error.response.status_code
        if status_code == 401:
            return 'Bad request'
        elif status_code == 404: 
            return f"'{description}': Data not found"
        elif status_code == 429: 
            return 'Riot Games API key rate limit reached'
        elif status_code == 403:
            return 'Riot Games API key expired'
        else:
            raise error

    def fetch_summoner(self, name_or_puuid, region=None, by_name=False):
        """
        Fetches summoner data by either name or puuid.
        
        :param name_or_puuid: The name or puuid of the summoner to fetch.
        :param region: (optional) The region of the summoner to fetch.
        :param by_name: (optional) Specify if name_or_puuid is a name or puuid. Default is False (puuid).
        
        :return: The summoner data.
        """
        try:
            if region:
                platform = Region.from_platform(region).value
            else:
                platform = self.region.get('platform').value
            if by_name:
                summoner = watcher.summoner.by_name(platform, name_or_puuid)
            else:
                summoner = watcher.summoner.by_puuid(platform, name_or_puuid)
                
            return {
                'id':           summoner['id'],
                'puuid':        summoner['puuid'],
                'name':         summoner['name'],
                'profileIcon':  DDragon.get_profile_icon(summoner['profileIconId']),
                'level':        f"Lvl. {summoner['summonerLevel']}"
            }
        except ApiError as error:
            return RiotFramework.handle_api_error(error, name_or_puuid)

    def fetch_league(self, encrypted_summoner_id: str):
        """
        Fetches ranked data by encrypted summoner id.

        :param encrypted_summoner_id: The encrypted summoner id of the summoner to fetch.
        
        :return: The summoner's ranked data.
        """
        try:
            fetched_league = watcher.league.by_summoner(self.region.get('platform').value, encrypted_summoner_id)
            calls = {0:'tier', 1:'rank', 2:'leaguePoints', 3:'wins', 4:'losses'}
            solo = {
                'tier':         None,
                'rank':         None,
                'leaguePoints': None,
                'wins':         None,
                'losses':       None,
            }
            flex = {
                'tier':         None,
                'rank':         None,
                'leaguePoints': None,
                'wins':         None,
                'losses':       None,
            }

            for i in range(len(fetched_league)):
                ranks = fetched_league[i]
                queue_type = ranks['queueType']
                if queue_type == 'RANKED_SOLO_5x5':
                    for j in range(len(calls)):
                        solo[calls[j]] = ranks[calls[j]]
                elif queue_type == 'RANKED_FLEX_SR':
                    for j in range(len(calls)):
                        flex[calls[j]] = ranks[calls[j]]
                        
            return {
                'solo': solo,
                'flex': flex
            }
        except ApiError as error:
            return RiotFramework.handle_api_error(error, encrypted_summoner_id)

    def fetch_mastery_score(self, encrypted_summoner_id: str):
        """
        Fetches summoner's mastery score. 

        :param encrypted_summoner_id: The encrypted summoner id of the summoner to fetch.
        
        :return: The summoner's mastery score.
        """
        try:
            return watcher.champion_mastery.scores_by_summoner(self.region.get('platform').value, encrypted_summoner_id)
        except ApiError as error:
            return RiotFramework.handle_api_error(error, encrypted_summoner_id)

    def fetch_masteries(self, encrypted_summoner_id: str):
        """
        Fetches summoner's top 3 champions.

        :param encrypted_summoner_id: The encrypted summoner id of the summoner to fetch.
        
        :return: The summoner's top 3 champions.
        """
        try:
            masteries = watcher.champion_mastery.by_summoner(self.region.get('platform').value, encrypted_summoner_id)[:3]
            ids, levels, points, names = [], [], [], []
            for champion in masteries:
                ids.append(champion['championId'])
                levels.append(f"Level_{champion['championLevel']}")
                points.append(f"{champion['championPoints']:,}")
            names = [Champion.from_id(id) for id in ids]
            
            return {
                'championNames':    names,
                'championLevels':   levels,
                'championPoints':   points
            }
        except ApiError as error:
            return RiotFramework.handle_api_error(error, encrypted_summoner_id)

    def fetch_challenges(self, puuid: str):
        """
        Fetches summoner's challenges.
        
        :param puuid: The puuid of the summoner to fetch.
        
        :return: The summoner's challenges.
        """
        try:
            challenges = watcher.challenges.by_puuid(self.region.get('platform').value, puuid)
            title_id = challenges.get('preferences', {}).get('title')
            title = Challenges.from_id(title_id) if title_id else None
            
            return {
                'title': title
            }
        except ApiError as error:
            return RiotFramework.handle_api_error(error, puuid)

    def fetch_match_list(self, puuid: str, count: int):
        """
        Fetches summoner's match list.
        
        :param puuid: The puuid of the summoner to fetch.
        
        :param count: The number of matches to fetch.
        """
        try:
            return watcher.match.matchlist_by_puuid(self.region['platform'].value, puuid, 0, count)
        except ApiError as error:
            return RiotFramework.handle_api_error(error, puuid)

    def fetch_match(self, match_id: str, puuid: str):
        """
        Fetches match data by match ID.

        :param match_id: The ID of the match to fetch.
        :param puuid: The puuid of the summoner to fetch.
        
        :return: The match data.
        """
        try:
            match = watcher.match.by_id(self.region.get('platform').value, match_id)

            """ Fetching game data """
            gameID = match['metadata']['matchId']
            index = gameID.find('_') + 1
            if index != -1: gameID = gameID[index:]

            gameEndTimestamp = round(match['info']['gameEndTimestamp'] / 1000)
            gameEnd = datetime.fromtimestamp(gameEndTimestamp).strftime('%d/%m/%Y')

            gameDuration = match['info']['gameDuration']
            delta_tmp = timedelta(seconds=gameDuration)
            delta_tmp = str(delta_tmp).split(':')
            if delta_tmp[0] == '0': gameDuration = delta_tmp[1] + ':' + delta_tmp[2]
            else: gameDuration = delta_tmp[0] + ':' + delta_tmp[1] + ':' + delta_tmp[2]

            queue_id = match['info']['queueId']
            Queue.from_id(queue_id)

            gameInfo = {
                'gameEndTimestamp': gameEndTimestamp,
                'gameEnd':          gameEnd,
                'gameDuration':     gameDuration,
                'gameMap':          Queue.map,
                'gameDescription':  Queue.description,
                'gameID':           gameID
            }

            """ Fetching team data """
            team1, team2, team_tmp = [], [], []
            for participant in match['info']['participants']:
                position = participant['teamPosition']
                if match['info']['gameMode'] == 'ARAM':
                    position = 'MIDDLE'
                player = {
                    'name':             participant['summonerName'],
                    'champion':         Champion.fix_name(participant['championName']),
                    'level':            participant['champLevel'],
                    'kills':            participant['kills'],
                    'deaths':           participant['deaths'],
                    'assists':          participant['assists'],
                    'gold':             participant['goldEarned'],
                    'cs':               participant['totalMinionsKilled'] + participant['neutralMinionsKilled'],
                    'items':            [participant['item0'], participant['item1'], participant['item2'], participant['item3'], participant['item4'], participant['item5'], participant['item6']],
                    'summonerSpells1':  participant['summoner1Id'], 
                    'summonerSpells2':  participant['summoner2Id'],
                    'rune':             participant['perks']['styles'][0]['selections'][0]['perk'],
                    'position':         position,
                    'win':              participant['win'],
                    'kda':              None,
                    'kp':               None,
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

            # Player's team is always team1
            if team_tmp[1]:
                tmp = team1
                team1 = team2
                team2 = tmp

            total_kills1 = total_deaths1 = total_assists1 = total_gold1 = 0
            total_kills2 = total_deaths2 = total_assists2 = total_gold2 = 0
            for i in range(len(team1)):
                total_kills1    += team1[i]['kills']
                total_deaths1   += team1[i]['deaths']
                total_assists1  += team1[i]['assists']
                total_gold1     += team1[i]['gold']
                total_kills2    += team2[i]['kills']
                total_deaths2   += team2[i]['deaths']
                total_assists2  += team2[i]['assists']
                total_gold2     += team2[i]['gold']

            runes_db = DDragon.get_runes_reforged()
            for i in range(len(team1)):
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
                'win':      team1[0]['win'],
                'kills':    total_kills1,
                'deaths':   total_deaths1,
                'assists':  total_assists1,
                'gold':     '{:,}'.format(total_gold1),
            }
            total_team2 = {
                'win':      team2[0]['win'],
                'kills':    total_kills2,
                'deaths':   total_deaths2,
                'assists':  total_assists2,
                'gold':     '{:,}'.format(total_gold2),
            }

            if team1[0]['win']:
                if match['info']['teams'][0]['win']: teamCase = True
                else: teamCase = False
            else:
                if match['info']['teams'][0]['win']: teamCase = False
                else: teamCase = True

            if teamCase:
                tmp_bans1       = match['info']['teams'][0]['bans']
                tmp_objectives1 = match['info']['teams'][0]['objectives']
                tmp_bans2       = match['info']['teams'][1]['bans']
                tmp_objectives2 = match['info']['teams'][1]['objectives']
            else:
                tmp_bans1       = match['info']['teams'][1]['bans']
                tmp_objectives1 = match['info']['teams'][1]['objectives']
                tmp_bans2       = match['info']['teams'][0]['bans']
                tmp_objectives2 = match['info']['teams'][0]['objectives']

            team1_bans, team2_bans = [], []
            try:
                champions_db = DDragon.get_champion()
                for i in range(len(tmp_bans1)):
                    if int(tmp_bans1[i]['championId']) == -1: team1_bans.append('None')
                    if int(tmp_bans2[i]['championId']) == -1: team2_bans.append('None')
                    for champion in champions_db:
                        if int(champions_db[champion]['key']) == int(tmp_bans1[i]['championId']):
                            team1_bans.append(champions_db[champion]['name'])
                        if int(champions_db[champion]['key']) == int(tmp_bans2[i]['championId']):
                            team2_bans.append(champions_db[champion]['name'])
            except: pass

            team1_objectives, team2_objectives = [], []
            calls = {0:'tower', 1:'inhibitor', 2:'baron', 3:'dragon', 4:'riftHerald'}
            for i in range(len(calls)):
                if tmp_objectives1[calls[i]]: team1_objectives.append(tmp_objectives1[calls[i]]['kills'])
                if tmp_objectives2[calls[i]]: team2_objectives.append(tmp_objectives2[calls[i]]['kills'])

            return (gameInfo, team_tmp[0], team1, team2, total_team1, total_team2, team1_bans, team2_bans, team1_objectives, team2_objectives)
        except ApiError as error:
            return RiotFramework.handle_api_error(error, match_id)


    
    def request_profile(self, name: str):
        """ Request profile of a summoner. """
        result = self.fetch_summoner(name_or_puuid=name, by_name=True)
        if isinstance(result, str):
            return result
        self.summoner = result

        result = self.fetch_league(self.summoner.get('id'))
        if isinstance(result, str): 
            return result
        self.league = result

        result = self.fetch_mastery_score(self.summoner.get('id'))
        if isinstance(result, str): 
            return result
        self.mastery_score = result

        result = self.fetch_masteries(self.summoner.get('id'))
        if isinstance(result, str): 
            return result
        self.masteries = result

        result = self.fetch_challenges(self.summoner.get('puuid'))
        if isinstance(result, str): 
            return result
        self.challenges = result

    def request_match_history(self):
        """ Request match history of a summoner. """
        if self.summoner is None: 
            return 'Summoner Name missing'

        result = self.fetch_match_list(self.summoner.get('puuid'), self.match_max)
        if isinstance(result, str): 
            return result
        self.match_list = result

        match = []
        try:
            for match_id in self.match_list:
                result = self.fetch_match(match_id, self.summoner.get('puuid'))
                if isinstance(result, str): 
                    return result
                match.append(result)
        except Exception as error:
            return (self.error_msg['001a'], self.error_msg['001b'])

        self.history = [match[i][0:2] for i in range(len(match))]
        self.match = match

        # Embed List of Match
        match_label = []
        match_emoji = []
        match_description = []
        for i in range(self.match_max):
            history = self.history[i]
            if history[1]['win']:
                title = 'VICTORY'
                if history[0]['gameMap'] == 'Howling Abyss':
                    match_emoji.append(Emoji.aram['victory'])
                else: 
                    match_emoji.append(Emoji.sr['victory'])
            else:
                title = 'DEFEAT \u200b  \u200b  \u200b '
                if history[0]['gameMap'] == 'Howling Abyss':
                    match_emoji.append(Emoji.aram['defeat'])
                else:
                    match_emoji.append(Emoji.sr['defeat'])

            name = Champion.fix_name(history[1]['champion'])
            match_label.append(f'{title} \u200b | \u200b {name} \u200b  \u200b  \u200b  \u200b {history[1]["kills"]} \u200b / \u200b {history[1]["deaths"]} \u200b / \u200b {history[1]["assists"]}')
            match_description.append(f'{history[0]["gameDescription"]} \u200b • \u200b {history[0]["gameDuration"]} \u200b • \u200b {history[0]["gameEnd"]}')

        self.match_select = [
            discord.SelectOption(label=match_label[0], description=match_description[0], emoji=match_emoji[0], value='1'),
            discord.SelectOption(label=match_label[1], description=match_description[1], emoji=match_emoji[1], value='2'),
            discord.SelectOption(label=match_label[2], description=match_description[2], emoji=match_emoji[2], value='3'),
            discord.SelectOption(label=match_label[3], description=match_description[3], emoji=match_emoji[3], value='4'),
            discord.SelectOption(label=match_label[4], description=match_description[4], emoji=match_emoji[4], value='5')
        ]

    def update_rank(self, player: list):
        """
        Update rank of a summoner.
        
        :param player: player data
        
        :return: match data if a new ranked match is found, else return error message
        """
        match_list = self.fetch_match_list(player.get('summoner').get('puuid'), 1)
        if not match_list:
            return "Match not found"

        match_id = match_list[0]
        if match_id == player.get('matchId'):
            return "No new match"
        player['matchId'] = match_id

        match = self.fetch_match(match_id, player.get('summoner').get('puuid'))
        if match[0].get('gameDescription') != "Ranked Solo/Duo":
            return "Not a ranked match"

        league = self.fetch_league(player.get('summoner').get('id')).get('solo')
        if isinstance(league, str):
            return league

        try:
            last_league     = player.get('league')
            current_league  = league
            try:
                last_lp     = int(last_league.get('leaguePoints'))
            except:
                last_lp     = 0
            try:
                current_lp  = int(current_league.get('leaguePoints'))
            except:
                current_lp  = 0
            lp              = abs(current_lp - last_lp)
            win             = match[1]['win']

            if win:
                result = f"+{lp} LP"
            else:
                result = f"-{lp} LP"

            if last_lp == 100 and current_lp == 100:
                result = "Promotion Series"

            if last_league.get('tier') == current_league.get('tier') == "None":
                if "PLACEMENTS" in player.get('resume'):
                    result = str_digit_add(player.get('resume'))
                if "PLACEMENTS 10/10" in player.get('resume'):
                    result = f"PLACED INTO {current_league.get('tier')} {current_league.get('rank')}"

            if last_league.get('rank') != current_league.get('rank'):
                if win:
                    result = f"PROMOTED TO {current_league.get('tier')} {current_league.get('rank')}"
                else:
                    result = f"DEMOTE TO {current_league.get('tier')} {current_league.get('rank')}"
        except Exception as error:
            result = "Error"

        player['league'] = league
        player['resume'] = result
        
        summoner = self.fetch_summoner(player.get('summoner').get('puuid'))
        if isinstance(summoner, str):
            return summoner
        player['summoner'] = summoner
        

        return match

    error_msg = {
        '001a':"\nWE DIDN'T FIND ANY MATCHES FOR THIS PLAYER.\nTHIS MIGHT BE BECAUSE...",
        '001b':f"{Emoji.blank}• This summoner hasn't played any ranked matches\n{Emoji.blank}• This summoner isn't fiends with the bot (and thus bot can't{Emoji.blank} \u200b  \u200b see their matches)\n{Emoji.blank}• This summoner hasn't played any matches since May 1st",
    }
