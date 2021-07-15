import discord
import requests
from datetime import *
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context, BadArgument
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from misc.utils import Utils
from firebase_admin import db

class MythicDungeons(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self)

    @cog_ext.cog_slash(
        name='mythic',
        description='Displays current week Mythic+ affixes',
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
        week_num = datetime.today()
                
        if region == 'us':
            resp = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region=us&locale=en').json()
        if region == 'eu':
            resp = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region=eu&locale=en').json()
        if region == 'tw':
            resp = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region=tw&locale=en').json()
        if region == 'kr':
            resp = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region=kr&locale=en').json()

        get_embed = self.get_affix_embed(
            week_num, [
            resp['title'],
            resp['affix_details'][0]['name'],
            resp['affix_details'][0]['description'],
            resp['affix_details'][1]['name'],
            resp['affix_details'][1]['description'],
            resp['affix_details'][2]['name'],
            resp['affix_details'][2]['description'],
            resp['affix_details'][3]['name'],
            resp['affix_details'][3]['description']
        ])
        await ctx.send(content=f'{ctx.author.mention}', embed=get_embed)

    def get_affix_embed(self, week, resp):

        embed = discord.Embed(
            title='Shadowlands Mythic+ Dungeon Affixes',
            description=f'For week #{week.strftime("%U")} we have: **{resp[0]}**',
            colour=discord.Colour.blue())
        embed.set_thumbnail(url='https://cdnassets.raider.io/images/brand/Icon_FullColor_Square.png')
        embed.add_field(name=resp[1], value=resp[2])
        embed.add_field(name=resp[3], value=resp[4])
        embed.add_field(name=resp[5], value=resp[6])
        embed.add_field(name=resp[7], value=resp[8])
        embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'Brought to you by {self.bot.user.display_name} and raider.io - {self.utils.get_time_parsed()}')
        return embed

    @cog_ext.cog_slash(
        name='raiderio',
        description="View any player's current IO score",
        options=[
            create_option(
                name='region',
                description='Select the region to search in',
                required=True,
                option_type=3,
                choices=[
                    create_choice(name='US', value='us'),
                    create_choice(name='EU', value='eu'),
                    create_choice(name='Korea', value='kr'),
                    create_choice(name='China', value='cn'),
                    create_choice(name='Taiwan', value='tw')]),
            create_option(
                name='server',
                description='Type the name of the server',
                required=True,
                option_type=3),
            create_option(
                name='player',
                description="Type the player's name",
                required=True,
                option_type=3)
        ]
    )
    async def raiderio(self, ctx: Context, region, server, player):
        resp = None

        if region == 'us':
            resp = requests.get('https://raider.io/api/v1/characters/profile?region=us&realm={}&name={}&fields=mythic_plus_scores_by_season%3Aprevious%3Acurrent'.format(server, player)).json()
            if 'error' in resp:
                raise BadArgument(resp['message'])
        if region == 'eu':
            resp = requests.get('https://raider.io/api/v1/characters/profile?region=eu&realm={}&name={}&fields=mythic_plus_scores_by_season%3Aprevious%3Acurrent'.format(server, player)).json()
            if 'error' in resp:
                raise BadArgument(resp['message'])
        if region == 'kr':
            resp = requests.get('https://raider.io/api/v1/characters/profile?region=kr&realm={}&name={}&fields=mythic_plus_scores_by_season%3Aprevious%3Acurrent'.format(server, player)).json()
            if 'error' in resp:
                raise BadArgument(resp['message'])
        if region == 'cn':
            resp = requests.get('https://raider.io/api/v1/characters/profile?region=cn&realm={}&name={}&fields=mythic_plus_scores_by_season%3Aprevious%3Acurrent'.format(server, player)).json()
            if 'error' in resp:
                raise BadArgument(resp['message'])
        if region == 'tw':
            resp = requests.get('https://raider.io/api/v1/characters/profile?region=tw&realm={}&name={}&fields=mythic_plus_scores_by_season%3Aprevious%3Acurrent'.format(server, player)).json()
            if 'error' in resp:
                raise BadArgument(resp['message'])

        get_embed = self.get_raiderio_embed([
            resp['name'],
            resp['class'],
            resp['thumbnail_url'],
            resp['region'],
            resp['realm'],
            str(resp['mythic_plus_scores_by_season'][0]['scores']['all']),
            str(resp['mythic_plus_scores_by_season'][1]['scores']['all']),
            resp['profile_url'],
            resp['active_spec_name']])

        await ctx.send(content=f'{ctx.author.mention}', embed=get_embed)

    def get_raiderio_embed(self, resp):

        embed = discord.Embed(
            title=f'RaiderIO Player Search for {resp[0]} on {resp[4]}-{resp[3]}',
            description=f'{resp[7]}\n\u200b',
            colour=discord.Colour.green())
        embed.set_thumbnail(url=resp[2])
        embed.add_field(name='Class', value=f'{resp[8]} {resp[1]}')
        embed.add_field(name='Current Season', value=f'{resp[6]}')
        embed.add_field(name='Previous Season', value=f'{resp[5]}')
        embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'Brought to you by {self.bot.user.display_name} and raider.io - {self.utils.get_time_parsed()}')
        return embed
    
    @raiderio.error
    async def raiderio_error(self, ctx: Context, error):
        if isinstance(error, BadArgument):
            await ctx.send(f'{ctx.author.mention} -> We ran into an issue: `{error}`. Please double check your spelling.')

def setup(bot):
    bot.add_cog(MythicDungeons(bot))