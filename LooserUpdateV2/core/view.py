import discord
from discord.ui import View, button, Select

from .resources import Emoji, Icon, Color
from .common import replace_spaces, percent, spacing
from .embed import Embed

from datastores.emoji import Item, Champion

class ViewProfile(discord.ui.View):
    """ View for the bot """

    def __init__(self, framework):
        super().__init__(timeout=None)
        self.framework = framework

    @discord.ui.button(
        label       = "OVERVIEW",
        style       = discord.ButtonStyle.grey,
        custom_id   = "overview"
    )
    async def overview(self, interaction: discord.Interaction, button: discord.ui.Button):
        for x in self.children:
            x.disabled = False
            if x.custom_id == "match_select": 
                x.disabled = True
                for y in x.options: y.default = False

        button.disabled = True
        embed = Embed.summoner_profile(self.framework.summoner, self.framework.region, self.framework.challenges, 
                                       self.framework.league, self.framework.mastery_score, self.framework.masteries)
        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(
        label       = "CHALLENGES", 
        style       = discord.ButtonStyle.grey, 
        custom_id   = "challenges"
    )
    async def challenges(self, interaction: discord.Interaction, button: discord.ui.Button):
        for x in self.children: 
            x.disabled = False
            if x.custom_id == "match_select":
                x.disabled = True
                for y in x.options: y.default = False

        button.disabled = True
        await interaction.response.edit_message(view=self, content="In development...")

    @discord.ui.button(
        label       = "MATCH HISTORY", 
        style       = discord.ButtonStyle.grey , 
        custom_id   = "match_history"
    )
    async def history(self, interaction: discord.Interaction, button: discord.ui.Button):
        for x in self.children:
            x.disabled = False
            if x.custom_id == "match_select":
                try: x.options = self.framework.match_select
                except: pass
                for y in x.options: y.default = False

        button.disabled = True
        embed = Embed.summoner_history(self.framework.history)
        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.select(
        placeholder = "MATCH DETAILS",
        options     = [
            discord.SelectOption(label="Match 1", value="1"),
            discord.SelectOption(label="Match 2", value="2"),
            discord.SelectOption(label="Match 3", value="3"),
            discord.SelectOption(label="Match 4", value="4"),
            discord.SelectOption(label="Match 5", value="5")
        ],
        disabled    = True,
        custom_id   = "match_select"
    )
    async def history_select(self, interaction=discord.Interaction, select=discord.ui.Select):
        for x in self.children: x.disabled = False
        for x in select.options: x.default = False
        select.options[int(select.values[0])-1].default = True
        embed = Embed.match(self.framework.match[int(select.values[0])-1])
        await interaction.response.edit_message(view=self, embed=embed)


class ViewUpdateMatch(discord.ui.View):
    """ View for the bot """

    def __init__(self, match, player):
        super().__init__(timeout=None)
        self.match_update = match
        self.player_update = player

    @discord.ui.button(label='MATCH DETAILS', style=discord.ButtonStyle.grey, custom_id='details')
    async def details(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ViewUpdateBack(self.match_update, self.player_update)
        embed = Embed.match(self.match_update)
        await interaction.response.edit_message(view=view, embed=embed)

class ViewUpdateBack(discord.ui.View):
    """ View for the bot """

    def __init__(self, match, player):
        super().__init__(timeout=None)
        self.match_update = match
        self.player_update = player

    @discord.ui.button(label='RETURN', style=discord.ButtonStyle.grey, custom_id='return')
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ViewUpdateMatch(self.match_update, self.player_update)
        embed = Embed.summoner_history_light(self.match_update, self.player_update)
        await interaction.response.edit_message(view=view, embed=embed)