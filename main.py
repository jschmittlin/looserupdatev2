import asyncio
import random

# Discord bot
import discord
from discord import app_commands
from discord.ext import tasks
import typing

# Riot RiotFramework
from riotFramework import RiotFramework
framework = RiotFramework()

# Discord Response
from response import MyEmbed, MyViewProfile, MyViewUpdateMatch

# data
from data import Emoji, UpdatePlayer, Region, ddragon, Item, ACTIVITIES
UpdatePlayer.load()

# Logging
import time
def log(message, level="INFO"):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print("[{}] [{:<8}] LooserUpdateV2: {}".format(current_time, level, message))

# dotenv
import os
from dotenv import load_dotenv
load_dotenv()

# Retrieve the token from the environment variable
MY_GUILD = discord.Object(id=os.getenv('GUILD_ID'))
ROLE_ADMIN_01 = int(os.getenv('ROLE_01'))
ROLE_ADMIN_02 = int(os.getenv('ROLE_02'))
CHANNEL = int(os.getenv('CHANNEL_ID'))

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
                embed = MyEmbed().history_light_embed(match, player)
                view = MyViewUpdateMatch(match, player)
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
        for item in Item.__undef__:
            url = ddragon.get_item(item)
            await Item.add_emoji(self, item, url)
            Item.remove_undefined(item)
            log("Add emoji: " + str(item))

    # Wait until the bot is ready before starting the task
    @update_item_undefined_task.before_loop
    async def before_update_item_undefined_task(self):
        await self.wait_until_ready()



client = MyClient()

@client.tree.command(
    name="set-region",
    description="Set the server's region."
)
@app_commands.describe(
    region="Region"
)
@app_commands.choices(
    region = Region.get_choices()
)
async def set_region(interaction: discord.Interaction, region: app_commands.Choice[str]):
    log("/set-region " + region.value)
    await interaction.response.defer()
    framework.set_region(region.value)
    embed = MyEmbed().region(framework.region)
    await interaction.followup.send(embed=embed)


@client.tree.command(
    name="profile",
    description="View selected summoner profile."
)
@app_commands.describe(
    name="Player Name"
)
async def profile(interaction: discord.Interaction, name: str):
    log("/profile " + name)
    await interaction.response.defer()
    embed = MyEmbed()
    framework.reset()

    result = framework.request_profile(name)
    if isinstance(result, str):
        return await interaction.followup.send(embed=embed.error(result))

    match_errors = False
    result = framework.request_match_history()
    if isinstance(result, str):
        return await interaction.followup.send(embed=embed.error(result))
    if isinstance(result, tuple):
        match_errors = True

    embed.init_data(framework.region, framework.summoner, framework.league, framework.mastery_score,
    framework.masteries, framework.challenges, framework.history, framework.match)

    if match_errors:
        embed_history = embed.error_match(result[0], result[1])
    else:
        embed_history = embed.history_embed()

    view = MyViewProfile()
    view.init_data(embed.profile_embed(), embed_history, framework.match_select, framework.match)
    view.children[0].disabled = True
    await interaction.followup.send(embed=embed.profile_embed(), view=view)


@client.tree.command(
    name="add-player",
    description="Add player to the Update list."
)
@app_commands.describe(
    name="Player Name",
    region="Region"
)
@app_commands.choices(
    region = Region.get_choices()
)
@app_commands.checks.has_any_role(ROLE_ADMIN_01, ROLE_ADMIN_02)
async def add_player(interaction: discord.Interaction, name: str, region: app_commands.Choice[str]):
    log("/add-player " + name + " " + region.value)
    embed = MyEmbed()
    data = UpdatePlayer.load()
    for player in data:
        if player.get('region') == region.value and player.get('summoner').get('name').lower() == name.lower():
            embed = embed.system("Player is already in the list.", "Please remove the player from the list first.")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

    if len(data) >= UpdatePlayer.max:
        embed = embed.system("Update list is full.", "Please remove some players from the list.")
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    await interaction.response.defer()

    summoner = framework.fetch_summoner(name_or_puuid=name, region=region.value, by_name=True)
    if isinstance(summoner, str):
        return await interaction.followup.send(embed=embed.error(summoner))

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

    await interaction.followup.send(embed=embed.success(f"{summoner.get('name')} #{region.value}", "Added to the Update list."))


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
        embed = MyEmbed().system("Player not found.", "Please check the player name.")
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    region = UpdatePlayer.get_region(name)
    UpdatePlayer.remove(name)
    framework.set_region(Region.europe_west.value[0])
    embed = MyEmbed().success(f"{name} #{region}", "Deleted from the Update list.")
    await interaction.response.send_message(embed=embed)


@client.tree.command(
    name="setting",
    description="View setting."
)
async def setting(interaction: discord.Interaction):
    log("/setting")
    region = framework.region.get('region')
    embed = MyEmbed().setting(region, UpdatePlayer.load(), UpdatePlayer.max)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(
    name="help",
    description="Shows the help menu."
)
async def help(interaction: discord.Interaction):
    log("/help")
    embed = MyEmbed().help()
    await interaction.response.send_message(embed=embed, ephemeral=True)


@help.error
async def help_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = MyEmbed().system("Error", error)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@profile.error
async def profile_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = MyEmbed().system("Error", error)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@set_region.error
async def set_region_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = MyEmbed().system("Error", error)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@add_player.error
async def add_player_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = MyEmbed().system("Permission denied", "You must get an admin to execute this command")
    await interaction.response.send_message(embed=embed, ephemeral=True)
        
@delete_player.error
async def delete_player_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = MyEmbed().system("Permission denied", "You must get an admin to execute this command")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@setting.error
async def setting_error(interaction: discord.Interaction, error: Exception):
    log(error)
    embed = MyEmbed().system("Error", error)
    await interaction.response.send_message(embed=embed, ephemeral=True)


client.run(os.getenv('TOKEN'))
