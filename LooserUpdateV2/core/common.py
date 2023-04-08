import urllib.parse
import time

from .resources import Emoji

def log(message, level="INFO"):
    """
    Log a message to the console with a given level.

    Parameters:
        message (str): The message to log.
        level (str): The level of the log (default is "INFO").

    Returns:
        None
    """
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print("[{}] [{:<8}] LooserUpdateV2: {}".format(current_time, level, message))

def replace_spaces(string: str):
    """
    Replaces spaces in a string with underscores.

    Args:
        string: A string that may contain spaces.

    Returns:
        A new string with all spaces replaced by underscores.
    """
    return string.replace(' ', '%20')

def percent(wins: int, losses: int) -> int:
    """
    Calculate the percentage of wins from total games played.

    Args:
        wins (int): The number of games won.
        losses (int): The number of games lost.

    Returns:
        int: The percentage of games won as an integer, rounded to the nearest whole number.

    """
    if wins is None or losses is None:
        return None
    return round((wins / (wins + losses)) * 100)

def spacing(tier: str, wins: int, losses: int) -> str:
    """
    Calculate the spacing between the rank and the winrate.

    Args:
        tier (str): The player's tier.
        wins (int): The number of wins.
        losses (int): The number of losses.

    Returns:
        str: A string representing the spacing between the rank and the winrate.

    """
    spaces = ""
    
    if tier == 'IRON' or tier == 'GOLD':
        spaces = f'{Emoji.blank}{Emoji.blank}{Emoji.blank} \u200b \u200b '
    elif tier == 'BRONZE' or tier == 'SILVER' or tier == 'MASTER':
        spaces = f'{Emoji.blank}{Emoji.blank}{Emoji.blank}'
    elif tier == 'PLATINUM' or tier == 'DIAMOND':
        spaces = f'{Emoji.blank} \u200b \u200b \u200b '
    elif tier == 'GRANDMASTER' or tier == 'CHALLENGER':
        return f'{Emoji.blank}'
    
    if wins > 99:
        spaces += ' \u200b '
    if losses > 99:
        spaces += ' \u200b '
        
    return spaces

def opgg(user: str, region: str) -> str:
    """
    Create the op.gg URL for a given user and region.

    Args:
        user (str): The username to search for on op.gg
        region (str): The region where the user's account is located

    Returns:
        str: The URL of the user's op.gg profile, or a default URL if user or region is missing.

    """
    default_url = "https://www.op.gg/"
    
    if not user or not region:
        return default_url
    
    try:
        encoded_user = urllib.parse.quote(user)
        opgg_url = f"https://www.op.gg/summoner/{region}/{encoded_user}"
    except:
        opgg_url = default_url
        
    return opgg_url

def str_digit_add(message: str) -> str:
    """Add 1 to the first number in a string.
    
    Args:
    message (str): A string that contains a number at the beginning
    
    Returns:
    str: A string with the number at the beginning incremented by 1
    """
    ranking = message.split("/")[0]
    
    if ranking.isdigit() and int(ranking) < 10:
        return message.replace(ranking, str(int(ranking) + 1))
    
    return message