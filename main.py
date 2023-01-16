import json
import requests
import datetime
import asyncio
import random

# Discord bot
import discord
from discord import app_commands
from discord.ext import commands, tasks

import os
from dotenv import load_dotenv
load_dotenv()

MY_GUILD = discord.Object(id=os.getenv('GUILD_ID'))
ROLE_ADMIN_01 = int(os.getenv('ROLE_01'))
ROLE_ADMIN_02 = int(os.getenv('ROLE_02'))

activities = [
    discord.Activity(type=discord.ActivityType.watching, name="you"),
    discord.Activity(type=discord.ActivityType.watching, name="Medhi put pressure on"),
    discord.Activity(type=discord.ActivityType.watching, name="Medhi be shadow ban"),
    discord.Activity(type=discord.ActivityType.watching, name="botlane feed"),
    discord.Activity(type=discord.ActivityType.watching, name="Jérôme farmer these jungle camps"),
    discord.Activity(type=discord.ActivityType.listening, name="Valentin raging"),
    discord.Activity(type=discord.ActivityType.listening, name="La déprime"),
    discord.Game(name="for /help"),
    discord.Game(name="at tracking down losers"),
    discord.Game(name="Blitzcrank's Poro Roundup"),
    discord.Game(name="Doom Bots"),
    discord.Game(name="to support KCorp !"),
]

class MyClient(discord.Client):
    def __init__(self):
        # creating text-based commands.
        super().__init__(intents=discord.Intents.default())
        # register application commands
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {client.user} (ID: {client.user.id})')
        print('------')

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

        # start the task to run in the background
        self.change_activity_task.start()

    @tasks.loop(seconds=600) # task runs every 10 minutes
    async def change_activity_task(self):
        activity = random.choice(activities)
        await self.change_presence(activity=activity)

    @change_activity_task.before_loop
    async def before_change_activity_task(self):
        await self.wait_until_ready()

    # TODO: Add a message when a player wins/loses a ranked game
        

client = MyClient()


# Riot Framework
from riotFramework import *

# Discord Response
from response import MyEmbed, MyView, Data

@client.tree.command(name="region", description="Sets the server's region.")
@app_commands.describe(region="Region")
@app_commands.choices(region = [
    app_commands.Choice(name="Brazil (BR)", value="BR"),
    app_commands.Choice(name="Europe Nordic & East (EUNE)", value="EUNE"),
    app_commands.Choice(name="Europe West (EUW)", value="EUW"),
    app_commands.Choice(name="Japan (JP)", value="JP"),
    app_commands.Choice(name="Korea (KR)", value="KR"),
    app_commands.Choice(name="Latin America North (LAN)", value="LAN"),
    app_commands.Choice(name="Latin America South (LAS)", value="LAS"),
    app_commands.Choice(name="North America (NA)", value="NA"),
    app_commands.Choice(name="Oceania (OCE)", value="OCE"),
    app_commands.Choice(name="Turkey (TR)", value="TR"),
    app_commands.Choice(name="Russia (RU)", value="RU"),
    app_commands.Choice(name="Philippines (PH)", value="PH"),
    app_commands.Choice(name="Singapore (SG)", value="SG"),
    app_commands.Choice(name="Thailand (TH)", value="TH"),
    app_commands.Choice(name="Taiwan (TW)", value="TW"),
    app_commands.Choice(name="Vietnam (VN)", value="VN"),
])
async def region(interaction: discord.Interaction, region: app_commands.Choice[str]):
    await interaction.response.defer()
    msg = set_region(region.value)
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    await interaction.followup.send(embed=MyEmbed.region(msg[0], msg[1], msg[2]))


@client.tree.command(name="profile", description="View selected summoner profile.")
@app_commands.describe(name="Player Name")
async def profile(interaction: discord.Interaction, name: str):
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    try:
        # Reset global variables
        resetGlobal()

        # Summoner Profile
        summoner = fetchSummoner(name)
        if isinstance(summoner, str): return await interaction.response.send_message(embed=MyEmbed.error(summoner), ephemeral=True)

        await interaction.response.defer()

        # Set summoner
        set_summoner(summoner)

        # Request Profile to Riot API
        request = requestProfile()
        if isinstance(request, str): return await interaction.followup.send(embed=MyEmbed.error(request))
        print('[Done] requestProfile')

        # Request Match History to Riot API
        request = requestMatchHistory()
        if isinstance(request, str): return await interaction.followup.send(embed=MyEmbed.error(request))
        print('[Done] requestMatchHistory')

        # Update Data
        Data.update(get_region(), get_summoner(), get_ranks(), get_masteryScore(), get_masteries(), get_challenges(), get_history(), get_match(), get_match_select())

        # Embed
        embed = MyEmbed.profile()

        # View
        view = MyView()
        view.children[0].disabled = True

        await interaction.followup.send(embed=embed, view=view)
    except Exception as error: await interaction.response.send_message(embed=MyEmbed.system("", error), ephemeral=True)


PLAYER = []
MAX_PLAYERS = 5
@client.tree.command(name="add-player", description="Add player to the Update list.")
@app_commands.describe(name="Player Name", region="Region")
@app_commands.choices(region = [
    app_commands.Choice(name="Brazil (BR)", value="BR"),
    app_commands.Choice(name="Europe Nordic & East (EUNE)", value="EUNE"),
    app_commands.Choice(name="Europe West (EUW)", value="EUW"),
    app_commands.Choice(name="Japan (JP)", value="JP"),
    app_commands.Choice(name="Korea (KR)", value="KR"),
    app_commands.Choice(name="Latin America North (LAN)", value="LAN"),
    app_commands.Choice(name="Latin America South (LAS)", value="LAS"),
    app_commands.Choice(name="North America (NA)", value="NA"),
    app_commands.Choice(name="Oceania (OCE)", value="OCE"),
    app_commands.Choice(name="Turkey (TR)", value="TR"),
    app_commands.Choice(name="Russia (RU)", value="RU"),
    app_commands.Choice(name="Philippines (PH)", value="PH"),
    app_commands.Choice(name="Singapore (SG)", value="SG"),
    app_commands.Choice(name="Thailand (TH)", value="TH"),
    app_commands.Choice(name="Taiwan (TW)", value="TW"),
    app_commands.Choice(name="Vietnam (VN)", value="VN"),
])
@app_commands.checks.has_any_role(ROLE_ADMIN_01, ROLE_ADMIN_02)
async def add_player(interaction: discord.Interaction, name: str, region: app_commands.Choice[str]):
    await interaction.response.defer()
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    try:
        if len(PLAYER) >= MAX_PLAYERS: return await interaction.followup.send(embed=MyEmbed.system("Update list is full.", "Please remove some players from the list."))

        # Summoner Profile
        summoner = fetchSummonerRegion(name, Region.from_platform(region.value).value)
        if isinstance(summoner, str): return await interaction.followup.send(embed=MyEmbed.error(summoner))

        # Set summoner
        rank = fetchRanks(summoner[0])[0]

        update_player = []
        update_player.append(region.value)
        update_player.append(summoner[2])
        update_player.append(summoner[0])
        update_player.append(summoner[1])
        rank.remove(rank[0])
        update_player.append(rank)
        
        PLAYER.append(update_player)

        await interaction.followup.send(embed=MyEmbed.success(f"{summoner[2]} #{region.value}", "Added to the Update list."))
    except Exception as error: await interaction.followup.send(embed=MyEmbed.system("", error), ephemeral=True)


@client.tree.command(name="setting", description="View setting.")
async def setting(interaction: discord.Interaction):
    region = Region.from_platform(get_region()).region
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    await interaction.response.send_message(embed=MyEmbed.setting((region.value[1], region.value[0]), PLAYER, MAX_PLAYERS), ephemeral=True)


@client.tree.command(name="delete-player", description="Delete all setting.")
@app_commands.checks.has_any_role(ROLE_ADMIN_01, ROLE_ADMIN_02)
async def delete_player(interaction: discord.Interaction):
    await interaction.response.defer()
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    PLAYER.clear()
    set_region(new_region="EUW") # Default Region
    await interaction.followup.send(embed=MyEmbed.success("All setting has been deleted.", " "))


@client.tree.command(name="test", description="test")
async def test(interaction: discord.Interaction, user: discord.User, *, message: str):
    Data.set_author(interaction.user.name, interaction.user.avatar.url)

    await interaction.response.send_message(embed=MyEmbed.success(f"Message has been sent to", " "), ephemeral=True)


@client.tree.command(name="dm", description="Send a message to a user.")
@app_commands.describe(user="User", message="Message")
@app_commands.checks.has_any_role(ROLE_ADMIN_01)
async def dm(interaction: discord.Interaction, user: discord.User, *, message: str):
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    await user.send(message)
    await interaction.response.send_message(embed=MyEmbed.success(f"Message has been sent to {user.name}", " "), ephemeral=True)


@client.tree.command(name="help", description="Shows the help menu.")
async def help(interaction: discord.Interaction):
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    await interaction.response.send_message(embed=MyEmbed.help(), ephemeral=True)


@add_player.error
async def add_player_error(interaction: discord.Interaction, error: Exception):
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    await interaction.response.send_message(embed=MyEmbed.system("Permission denied", "You must get an admin to execute this command"), ephemeral=True)
        
@delete_player.error
async def delete_player_error(interaction: discord.Interaction, error: Exception):
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    await interaction.response.send_message(embed=MyEmbed.system("Permission denied", "You must get an admin to execute this command"), ephemeral=True)

@setting.error
async def setting_error(interaction: discord.Interaction, error: Exception):
    Data.set_author(interaction.user.name, interaction.user.avatar.url)
    await interaction.response.send_message(embed=MyEmbed.system("Error", error), ephemeral=True)


client.run(os.getenv('TOKEN'))
