import json
import requests
import datetime
import asyncio
import random

# Discord bot
import discord
from discord import app_commands
from discord.ext import commands, tasks

EMO = discord.Object(id=1039594104297881720)
MY_GUILD = discord.Object(id=469156433502404639)

activities = [
    discord.Activity(type=discord.ActivityType.watching, name="you"),
    discord.Activity(type=discord.ActivityType.watching, name="Medhi put pressure on"),
    discord.Activity(type=discord.ActivityType.watching, name="botlane feed"),
    discord.Activity(type=discord.ActivityType.watching, name="LoLEsports"),
    discord.Activity(type=discord.ActivityType.watching, name="Jérôme farmer these jungle camps"),
    discord.Activity(type=discord.ActivityType.listening, name="Valentin raging"),
    discord.Activity(type=discord.ActivityType.listening, name="La déprime"),
    discord.Activity(type=discord.ActivityType.listening, name="them scream"),
    discord.Game(name="for /help"),
    discord.Game(name="at tracking down losers"),
    discord.Game(name="Blitzcrank's Poro Roundup"),
    discord.Game(name="Doom Bots"),
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
    app_commands.Choice(name="Europe Nordic & East (EUNE)", value="EUN"),
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
    await interaction.followup.send(embed=MyEmbed.success(msg))


@client.tree.command(name="profile", description="View selected summoner profile.")
@app_commands.describe(name="Player Name")
async def profile(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    try:
        # Reset global variables
        resetGlobal()

        # Summoner Profile
        summoner = fetchSummoner(name)
        if isinstance(summoner, str): return await interaction.followup.send(embed=MyEmbed.error(summoner))

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

        # Set Author
        Data.set_author(interaction.user.name, interaction.user.avatar.url)

        # Embed
        embed = MyEmbed.profile()

        # View
        view = MyView()
        view.children[0].disabled = True

        await interaction.followup.send(embed=embed, view=view)
    except Exception as error: await interaction.followup.send(embed=MyEmbed.system("", error))


player = []
@client.tree.command(name="add-player", description="Add player to the Update list.")
@app_commands.describe(name="Player Name", region="Region")
@app_commands.choices(region = [
    app_commands.Choice(name="Brazil (BR)", value="BR"),
    app_commands.Choice(name="Europe Nordic & East (EUNE)", value="EUN"),
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
async def add_player(interaction: discord.Interaction, name: str, region: app_commands.Choice[str]):
    await interaction.response.defer()
    try:
        # Summoner Profile
        summoner = fetchSummoner(name)
        if isinstance(summoner, str): return await interaction.followup.send(embed=MyEmbed.error(summoner))

        # Set summoner
        player.append(summoner)

        Data.set_author(interaction.user.name, interaction.user.avatar.url)
        await interaction.followup.send(embed=MyEmbed.success(f"Added {summoner[2]} to the Update list."))
    except Exception as error: await interaction.followup.send(embed=MyEmbed.system("", error))
        

@client.tree.command(name="update", description="View selected summoner LP in ranked.")
async def update(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(embed=MyEmbed.system("Update", "This command is currently under development."))


@client.tree.command(name="setting", description="View setting.")
async def setting(interaction: discord.Interaction):
    await interaction.response.defer()
    region = get_region()
    await interaction.followup.send(embed=MyEmbed.system(region, player))


@client.tree.command(name="delete-setting", description="Delete all setting.")
async def delete_setting(interaction: discord.Interaction):
    await interaction.response.defer()
    player.clear()
    set_region(new_region="EUW") # Default Region
    await interaction.followup.send(embed=MyEmbed.success("All setting has been deleted."))


@client.tree.command(name="help", description="Shows the help menu.")
async def help(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(embed=MyEmbed.system("Help", "This command is currently under development."))




client.run('MTAzNzM5NTUwNjY5NzA3Njg3Nw.G_uliL.DpvHBTtKz7enx15s5v7qtpi4NjMOr-_a6eCCIs')
