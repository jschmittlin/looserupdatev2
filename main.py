import asyncio
import random

# Discord bot
import discord
from discord import app_commands
from discord.ext import tasks

# Riot RiotFramework
from riotFramework import RiotFramework
framework = RiotFramework()

# Discord Response
from response import MyEmbed, MyViewProfile, MyViewUpdateMatch

# data
from data import UpdatePlayer, Region, ddragon, item_undefined
UpdatePlayer.load()

# dotenv
import os
from dotenv import load_dotenv
load_dotenv()

# Logging
import time
def log(message, level="INFO"):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print("[{}] [{:<8}] LooserUpdateV2: {}".format(current_time, level, message))

# Retrieve the token from the environment variable
MY_GUILD = discord.Object(id=os.getenv('GUILD_ID'))
ROLE_ADMIN_01 = int(os.getenv('ROLE_01'))
ROLE_ADMIN_02 = int(os.getenv('ROLE_02'))
CHANNEL = int(os.getenv('CHANNEL_ID'))
USER = int(os.getenv('USER_01'))

# List of activities
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
        self.send_item_undefined_task.start()

    # Task to change the bot's activity
    @tasks.loop(seconds=1200) # Runs every 20 minutes
    async def change_activity_task(self):
        activity = random.choice(activities)
        await self.change_presence(activity=activity)

    # Wait until the bot is ready before starting the task
    @change_activity_task.before_loop
    async def before_change_activity_task(self):
        await self.wait_until_ready()

    # Task to update the player's rank
    @tasks.loop(seconds=60) # Runs every 1 minutes
    async def update_player_task(self):
        channel = self.get_channel(CHANNEL)
        data = UpdatePlayer.load()
        new_data = []
        for player in data:
            match = framework.update_rank(player)
            new_data.append(player)
            if not isinstance(match, str):
                embed = MyEmbed().history_light_embed(match, player)
                view = MyViewUpdateMatch(match, player)
                await channel.send(embed=embed, view=view)
        UpdatePlayer.save(new_data)

    # Wait until the bot is ready before starting the task
    @update_player_task.before_loop
    async def before_update_player_task(self):
        await self.wait_until_ready()

    # Task to send dm to user when an item is missing
    already_send = []
    @tasks.loop(seconds=3600) # Runs every 1 hour
    async def send_item_undefined_task(self):
        for item in item_undefined:
            if item in self.already_send:
                continue
            self.already_send.append(item)
            url = ddragon.get_item(item)
            user = await self.fetch_user(USER)
            await user.send("Item {} missing: {}".format(item, url))

    # Wait until the bot is ready before starting the task
    @send_item_undefined_task.before_loop
    async def before_send_item_undefined_task(self):
        await self.wait_until_ready()




client = MyClient()

@client.tree.command(name="set-region", description="Set the server's region.")
@app_commands.describe(region="Region")
@app_commands.choices(region = [
    app_commands.Choice(name="Brazil (BR)", value=Region.brazil.value[0]),
    app_commands.Choice(name="Europe Nordic & East (EUNE)", value=Region.europe_north_east.value[0]),
    app_commands.Choice(name="Europe West (EUW)", value=Region.europe_west.value[0]),
    app_commands.Choice(name="Japan (JP)", value=Region.japan.value[0]),
    app_commands.Choice(name="Korea (KR)", value=Region.korea.value[0]),
    app_commands.Choice(name="Latin America North (LAN)", value=Region.latin_america_north.value[0]),
    app_commands.Choice(name="Latin America South (LAS)", value=Region.latin_america_south.value[0]),
    app_commands.Choice(name="North America (NA)", value=Region.north_america.value[0]),
    app_commands.Choice(name="Oceania (OCE)", value=Region.oceania.value[0]),
    app_commands.Choice(name="Turkey (TR)", value=Region.turkey.value[0]),
    app_commands.Choice(name="Russia (RU)", value=Region.russia.value[0]),
    app_commands.Choice(name="Philippines (PH)", value=Region.philippines.value[0]),
    app_commands.Choice(name="Singapore (SG)", value=Region.singapore.value[0]),
    app_commands.Choice(name="Thailand (TH)", value=Region.thailand.value[0]),
    app_commands.Choice(name="Taiwan (TW)", value=Region.taiwan.value[0]),
    app_commands.Choice(name="Vietnam (VN)", value=Region.vietnam.value[0]),
])
async def set_region(interaction: discord.Interaction, region: app_commands.Choice[str]):
    log("/set-region " + region.value)
    await interaction.response.defer()
    framework.set_region(region.value)
    embed = MyEmbed().region(framework.region)
    await interaction.followup.send(embed=embed)


@client.tree.command(name="profile", description="View selected summoner profile.")
@app_commands.describe(name="Player Name")
async def profile(interaction: discord.Interaction, name: str):
    log("/profile " + name)
    await interaction.response.defer()
    embed = MyEmbed()
    try:
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

        embed.init_data(framework.region, framework.summoner_info, framework.ranks, framework.mastery_score,
        framework.masteries, framework.challenges, framework.history, framework.match)

        if match_errors:
            embed_history = embed.error_match(result[0], result[1])
        else:
            embed_history = embed.history_embed()

        view = MyViewProfile()
        view.init_data(embed.profile_embed(), embed_history, framework.match_select, framework.match)
        view.children[0].disabled = True
        await interaction.followup.send(embed=embed.profile_embed(), view=view)
    except Exception as error:
        await interaction.followup.send(embed=MyEmbed.error(error))


@client.tree.command(name="add-player", description="Add player to the Update list.")
@app_commands.describe(name="Player Name", region="Region")
@app_commands.choices(region = [
    app_commands.Choice(name="Brazil (BR)", value=Region.brazil.value[0]),
    app_commands.Choice(name="Europe Nordic & East (EUNE)", value=Region.europe_north_east.value[0]),
    app_commands.Choice(name="Europe West (EUW)", value=Region.europe_west.value[0]),
    app_commands.Choice(name="Japan (JP)", value=Region.japan.value[0]),
    app_commands.Choice(name="Korea (KR)", value=Region.korea.value[0]),
    app_commands.Choice(name="Latin America North (LAN)", value=Region.latin_america_north.value[0]),
    app_commands.Choice(name="Latin America South (LAS)", value=Region.latin_america_south.value[0]),
    app_commands.Choice(name="North America (NA)", value=Region.north_america.value[0]),
    app_commands.Choice(name="Oceania (OCE)", value=Region.oceania.value[0]),
    app_commands.Choice(name="Turkey (TR)", value=Region.turkey.value[0]),
    app_commands.Choice(name="Russia (RU)", value=Region.russia.value[0]),
    app_commands.Choice(name="Philippines (PH)", value=Region.philippines.value[0]),
    app_commands.Choice(name="Singapore (SG)", value=Region.singapore.value[0]),
    app_commands.Choice(name="Thailand (TH)", value=Region.thailand.value[0]),
    app_commands.Choice(name="Taiwan (TW)", value=Region.taiwan.value[0]),
    app_commands.Choice(name="Vietnam (VN)", value=Region.vietnam.value[0]),
])
@app_commands.checks.has_any_role(ROLE_ADMIN_01, ROLE_ADMIN_02)
async def add_player(interaction: discord.Interaction, name: str, region: app_commands.Choice[str]):
    log("/add-player " + name + " " + region.value)
    embed = MyEmbed()
    data = UpdatePlayer.load()
    for player in data:
        if player[0] == region.value and player[1].lower() == name.lower():
            return await interaction.response.send_message(embed=embed.system("Player is already in the list.", "Please remove the player from the list first."), ephemeral=True)

    try:
        if len(data) >= UpdatePlayer.max:
            return await interaction.response.send_message(embed=embed.system("Update list is full.", "Please remove some players from the list."), ephemeral=True)
        
        await interaction.response.defer()

        summoner = framework.fetch_summoner(name_or_puuid=name, region=region.value, by_name=True)
        if isinstance(summoner, str):
            return await interaction.followup.send(embed=embed.error(summoner))

        rank = framework.fetch_ranks(summoner.get('id')).get('solo')[1:]
        try: match_id = framework.fetch_match_list(summoner.get('puuid'), 1)[0]
        except: match_id = None

        player = []
        player.append(region.value)                     # 0: Region
        player.append(summoner.get('name'))             # 1: Summoner Name
        player.append(summoner.get('id'))               # 2: ID
        player.append(summoner.get('puuid'))            # 3: PUUID
        player.append(rank)                             # 4: Ranks
        player.append(match_id)                         # 5: Match ID
        player.append(summoner.get('profile_icon'))     # 6: Profile Icon
        player.append("PLACEMENTS 0/10")                # 7: Resume Games Ranks
        
        data.append(player)
        UpdatePlayer.save(data)

        await interaction.followup.send(embed=embed.success(f"{summoner.get('name')} #{region.value}", "Added to the Update list."))
    except Exception as error:
        await interaction.followup.send(embed=embed.error(error))


@client.tree.command(name="delete-player", description="Delete all players from the Update list.")
@app_commands.checks.has_any_role(ROLE_ADMIN_01, ROLE_ADMIN_02)
async def delete_player(interaction: discord.Interaction):
    log("/delete-player")
    UpdatePlayer.delete()
    framework.set_region(Region.europe_west.value[0])
    embed = MyEmbed().success("All players has been deleted.", " ")
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="setting", description="View setting.")
async def setting(interaction: discord.Interaction):
    log("/setting")
    region = framework.region.get('region')
    embed = MyEmbed().setting((region.value[1], region.value[0]), UpdatePlayer.load(), UpdatePlayer.max)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name="dm", description="Send a message to a user.")
@app_commands.describe(user="User", message="Message")
@app_commands.checks.has_any_role(ROLE_ADMIN_01)
async def dm(interaction: discord.Interaction, user: discord.User, *, message: str):
    log("/dm " + user.name + " " + message)
    await user.send(message)
    embed = MyEmbed().success(f"Message has been sent to {user.name}", message)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name="help", description="Shows the help menu.")
async def help(interaction: discord.Interaction):
    log("/help")
    embed = MyEmbed().help()
    await interaction.response.send_message(embed=embed, ephemeral=True)


@add_player.error
async def add_player_error(interaction: discord.Interaction, error: Exception):
    embed = MyEmbed().system("Permission denied", "You must get an admin to execute this command")
    await interaction.response.send_message(embed=embed, ephemeral=True)
        
@delete_player.error
async def delete_player_error(interaction: discord.Interaction, error: Exception):
    embed = MyEmbed().system("Permission denied", "You must get an admin to execute this command")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@setting.error
async def setting_error(interaction: discord.Interaction, error: Exception):
    embed = MyEmbed().system("Error", error)
    await interaction.response.send_message(embed=embed, ephemeral=True)


client.run(os.getenv('TOKEN'))
