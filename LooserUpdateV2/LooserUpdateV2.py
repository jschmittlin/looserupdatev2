import asyncio
import random
import copy

import discord
from discord import app_commands
from discord.ext import tasks
import typing

import os
from dotenv import load_dotenv

from core.common import log
from core.data import Region
from core.updatePlayer import UpdatePlayer
from core.resources import ACTIVITIES
from core.embed import Embed
from core.view import ViewProfile, ViewUpdateMatch

from datastores.riotFramework import RiotFramework
from datastores.emoji import Item
from datastores.ddragon import DDragon

framework = RiotFramework()
UpdatePlayer.load()
load_dotenv()

MY_GUILD        = discord.Object(id=os.getenv('GUILD_ID'))
ROLE_ADMIN_01   = int(os.getenv('ROLE_01'))
ROLE_ADMIN_02   = int(os.getenv('ROLE_02'))
CHANNEL         = int(os.getenv('CHANNEL_ID'))

class MyClient(discord.Client):
    def __init__(self):
        # Creating text-based commands.
        super().__init__(intents=discord.Intents.default())
        # Register application commands
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        log("logged in as {} (ID: {})".format(self.user, self.user.id))

    async def setup_hook(self):
        # Copy global commands to guild
        self.tree.copy_global_to(guild=MY_GUILD)
        # Synchronize guild commands
        await self.tree.sync(guild=MY_GUILD)

        # Start background tasks
        self.change_activity_task.start()
        self.update_player_task.start()
        self.update_item_undefined_task.start()

    # Task to change the bot's activity
    @tasks.loop(seconds=1200) # Runs every 20 minutes
    async def change_activity_task(self):
        activity = random.choice(ACTIVITIES)
        await self.change_presence(activity=activity)

    # Wait until the bot is ready before starting the task
    @change_activity_task.before_loop
    async def before_change_activity_task(self):
        await self.wait_until_ready()

    # Task to update the player's rank
    @tasks.loop(seconds=60) # Runs every 1 minutes
    async def update_player_task(self):
        data = UpdatePlayer.load()
        new_data = []
        for player in data:
            match = framework.update_rank(player)
            new_data.append(player)
            if not isinstance(match, str):
                log("Update: " + player.get('summoner').get('name'))
                channel = self.get_channel(CHANNEL)
                embed = Embed.summoner_history_light(match, player)
                view = ViewUpdateMatch(match, player)
                try:
                    await channel.send(embed=embed, view=view)
                except Exception as e:
                    log(str(e), "ERROR")
        UpdatePlayer.save(new_data)

    # Wait until the bot is ready before starting the task
    @update_player_task.before_loop
    async def before_update_player_task(self):
        await self.wait_until_ready()

    # Task to add emoji to items that are not defined
    @tasks.loop(seconds=60) # Runs every 1 minutes
    async def update_item_undefined_task(self):
        copy_undefined = Item._undefined.copy()
        for item_id in copy_undefined:
            url = DDragon.get_item(item_id)
            await Item.add_emoji(self, item_id, url)
            Item.remove_undefined(item_id)

    # Wait until the bot is ready before starting the task
    @update_item_undefined_task.before_loop
    async def before_update_item_undefined_task(self):
        await self.wait_until_ready()



client = MyClient()


"""
    Global commands
"""

COMMANDS = {
            "help"          : "List of commands",
            "profile"       : "View selected summoner profile",
            "set-region"    : "Set the server's region",
            "setting"       : "View setting",
            "add-player"    : "Add player to the Update list",
            "delete-player" : "Delete player from the Update list"
        }

@client.tree.command(
    name        = "help",
    description = "Shows the help menu."
)
async def help(interaction: discord.Interaction):
    log("/help")
    await interaction.response.send_message(embed=Embed.help(COMMANDS), ephemeral=True)
    
    
@client.tree.command(
    name        = "profile",
    description = "View selected summoner profile."
)
@app_commands.describe(
    name        = "Player Name"
)
async def profile(interaction: discord.Interaction, name: str):
    log("/profile " + name)
    await interaction.response.defer()
    
    framework.reset()

    result = framework.request_profile(name)
    if isinstance(result, str):
        return await interaction.followup.send(embed=Embed.error(result))

    embed_summoner_profile = Embed.summoner_profile(framework.summoner, framework.region, framework.challenges,
                                                      framework.league, framework.mastery_score, framework.masteries)
    
    match_errors = False
    result = framework.request_match_history()
    if isinstance(result, str):
        return await interaction.followup.send(embed=Embed.error(result))
    if isinstance(result, tuple):
        match_errors = True
    
    if match_errors:
        embed_summoner_history = Embed.error_match(result[0], result[1])
    else:
        embed_summoner_history = Embed.summoner_history(framework.history)

    copy_framework = copy.deepcopy(framework)
    view = ViewProfile(copy_framework)
    view.children[0].disabled = True
    
    await interaction.followup.send(embed=embed_summoner_profile, view=view)
    
@client.tree.command(
    name        = "set-region",
    description = "Set the server's region."
)
@app_commands.describe(
    region      = "Region"
)
@app_commands.choices(
    region      = Region.get_choices()
)
async def set_region(interaction: discord.Interaction, region: app_commands.Choice[str]):
    log("/set-region " + region.value)
    await interaction.response.defer()
    framework.set_region(region.value)
    await interaction.followup.send(embed=Embed.region(framework.region))

@client.tree.command(
    name        = "add-player",
    description = "Add player to the Update list."
)
@app_commands.describe(
    name        = "Player Name",
    region      = "Region"
)
@app_commands.choices(
    region      = Region.get_choices()
)
@app_commands.checks.has_any_role(ROLE_ADMIN_01, ROLE_ADMIN_02)
async def add_player(interaction: discord.Interaction, name: str, region: app_commands.Choice[str]):
    log("/add-player " + name + " " + region.value)
    data = UpdatePlayer.load()
    for player in data:
        if player.get('region') == region.value and player.get('summoner').get('name').lower() == name.lower():
            embed = Embed.system("Player is already in the list.", "Please remove the player from the list first.")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

    if len(data) >= UpdatePlayer.max:
        embed = Embed.system("Update list is full.", "Please remove some players from the list.")
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    await interaction.response.defer()

    summoner = framework.fetch_summoner(name_or_puuid=name, region=region.value, by_name=True)
    if isinstance(summoner, str):
        return await interaction.followup.send(embed=Embed.error(summoner))

    league = framework.fetch_league(summoner.get('id')).get('solo')
    try: match_id = framework.fetch_match_list(summoner.get('puuid'), 1)[0]
    except: match_id = None

    player = {
        "region": region.value,
        "summoner": summoner,
        "league": league,
        "matchId": match_id,
        "resume": "PLACEMENTS 0/10"
    }
    
    data.append(player)
    UpdatePlayer.save(data)

    await interaction.followup.send(embed=Embed.success(f"{summoner.get('name')} #{region.value}", "Added to the Update list."))


async def delete_player_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    data = []
    for player in UpdatePlayer.get_summoner_names():
        if current.lower() in player.lower():
            data.append(app_commands.Choice(name=f"{player} #{UpdatePlayer.get_region(player)}", value=player))
    return data

@client.tree.command(
    name="delete-player",
    description="Delete all players from the Update list."
)
@app_commands.describe(
    name = "Player Name"
)
@app_commands.autocomplete(name=delete_player_autocomplete)
@app_commands.checks.has_any_role(ROLE_ADMIN_01, ROLE_ADMIN_02)
async def delete_player(interaction: discord.Interaction, name: str):
    log("/delete-player " + name)
    if name not in UpdatePlayer.get_summoner_names():
        embed = Embed.system("Player not found.", "Please check the player name.")
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    region = UpdatePlayer.get_region(name)
    UpdatePlayer.remove(name)
    framework.set_region(Region.europe_west.value[0])
    embed = Embed.success(f"{name} #{region}", "Deleted from the Update list.")
    await interaction.response.send_message(embed=embed)

@client.tree.command(
    name="setting",
    description="View setting."
)
async def setting(interaction: discord.Interaction):
    log("/setting")
    region = framework.region.get('region')
    embed = Embed.setting(region, UpdatePlayer.load(), UpdatePlayer.max)
    await interaction.response.send_message(embed=embed, ephemeral=True)


"""
    Error handling
"""

@help.error
async def help_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = Embed.error("Command 'help'")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@profile.error
async def profile_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = Embed.error("Command 'profile'")
    await interaction.followup.send(embed=embed)

@set_region.error
async def set_region_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = Embed.error("Command 'set-region'")
    await interaction.followup.send(embed=embed)

@setting.error
async def setting_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = Embed.error("Command 'setting'")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
@add_player.error
async def add_player_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = Embed.system("Permission denied", "You must get an admin to execute this command")
    await interaction.followup.send(embed=embed)
        
@delete_player.error
async def delete_player_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = Embed.system("Permission denied", "You must get an admin to execute this command")
    await interaction.followup.send(embed=embed)


client.run(os.getenv('TOKEN'))
