import discord
import requests
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from misc.firebase import DBConnection
from misc.utils import Utils
from firebase_admin import db

class MythicDungeons(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='mythic',
        description='Displays current week Mythic+ affixes',
        guild_ids=[662464939469963285],
        options=[
            create_option(
                name='region',
                description='Select which region',
                required=True,
                option_type=3,
                choices=[
                    create_choice(name='US', value='us'),
                    create_choice(name='EU', value='eu'),
                    create_choice(name='Korea', value='kr'),
                    create_choice(name='Taiwan', value='tw')])
        ])
    async def get_affixes(self, ctx: Context, region):
        
        if region == 'us':
            resp = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region=us&locale=en').json()
            print(resp)

def setup(bot):
    bot.add_cog(MythicDungeons(bot))