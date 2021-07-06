import discord
import os
import requests
from random import randint as random
from discord import Member
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from misc.utils import Utils
from datetime import datetime as dt


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self)

    # Invite Command

    @cog_ext.cog_slash(
        name='invite',
        description='Create an invite',
        guild_ids=[662464939469963285],
        options=[
            create_option(
                name='limit',
                description='How many seconds should this invite be active for? 0=forever, 300=5 mins.',
                required=False,
                option_type=3
            ),
            create_option(
                name='uses',
                description='How many uses for this invite? 0=unlimited',
                required=False,
                option_type=3
            )]
    )
    async def link(self, ctx: Context, limit=0, uses=0):
        inv_link = await ctx.channel.create_invite(max_age=limit, max_uses=uses, unique=True)
        if limit == 0 and uses == 0:
            await ctx.send(content=f'{ctx.author.mention} -> Here is your link.\n\n{inv_link}', delete_after=60)
        else:
            m, s = divmod(float(limit), 60)
            if uses == 0:
                await ctx.send(content=f'{ctx.author.mention} -> Here is your link.\n\nRemember, the link is active for `{int(m)}m {int(s)}s`.\n\n{inv_link}', delete_after=60)
            else:
                await ctx.send(content=f'{ctx.author.mention} -> Here is your link.\n\nRemember, the link is active for `{int(m)}m {int(s)}s` and can be used `{uses}` times.\n\n{inv_link}', delete_after=60)

    # WoW Token Price Getter

    @cog_ext.cog_slash(
        name='wowtoken',
        description='Displays the current WoW token price.',
        guild_ids=[662464939469963285],
        options=[
            create_option(
                name='region',
                description='Select the region',
                required=True,
                option_type=3,
                choices=[
                    create_choice(
                        name='US',
                        value='us'
                    ),
                    create_choice(
                        name='EU',
                        value='eu'
                    ),
                    create_choice(
                        name='China',
                        value='china'
                    ),
                    create_choice(
                        name='Korea',
                        value='korea'
                    ),
                    create_choice(
                        name='Taiwan',
                        value='taiwan'
                    )])
        ])
    async def wow_token(self, ctx: SlashContext, region):
        grant = self.utils.blizzard_access_token()
        resp = None

        if region == 'us':
            resp = requests.get('https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US&access_token=%s' % grant).json()
        if region == 'eu':
            resp = requests.get('https://eu.api.blizzard.com/data/wow/token/index?namespace=dynamic-eu&locale=en_EU&access_token=%s' % grant).json()
        if region == 'china':
            resp = requests.get('https://gateway.battlenet.com.cn/data/wow/token/index?namespace=dynamic-cn&locale=zh_CN&access_token=%s' % grant).json()
        if region == 'korea':
            resp = requests.get('https://kr.api.blizzard.com/data/wow/token/index?namespace=dynamic-kr&locale=en_KR&access_token=%s' % grant).json()
        if region == 'taiwan':
            resp = requests.get('https://tw.api.blizzard.com/data/wow/token/index?namespace=dynamic-tw&locale=en_TW&access_token=%s' % grant).json()
        
        price = str(resp['price'])[:-4]
        price = [i for i in price]
        price.insert(3,',')
        if region == 'us' or region == 'eu':
            await ctx.send(content=f"{ctx.author.mention} -> WoW Token Price in the `{region.upper()}` is currently `{''.join(price)}g `")
        else:
            await ctx.send(content=f"{ctx.author.mention} -> WoW Token Price in `{region.capitalize()}` is currently `{''.join(price)}g `")

    # Ranks Command

    @cog_ext.cog_slash(
        name='ranks',
        description='Displays current DPS ranks in raid.',
        guild_ids=[662464939469963285])
    async def ranks(self, ctx: Context):
        await ctx.send(f"{ctx.author.mention} -> Here are the current DPS ranks.\nhttps://i.imgur.com/qXzph89.png")

    # 8-ball Command

    @cog_ext.cog_slash(
        name='8ball',
        description='Ask the 8Ball a question',
        guild_ids=[662464939469963285],
        options=[
            create_option(
                name='question',
                description='Ask your question',
                required=True,
                option_type=3)
                ])
    async def eight_ball(self, ctx: SlashContext, question):

        answers = [
            'Maybe.',
            'No.',
            'HAHAHAHAH, in your dreams.',
            'Likely not.',
            'Possibly.',
            'YES! ABSOLUTELY!',
            'You wish.',
            'Never.',
            'Yup.',
            'I believe so.',
            'What do you think?',
            'My answer starts with a Y and ends in S.',
            'Spell it out with me, N... O...',
            'You wasted my time with this question?',
            "I don't know, but Jaina is a Dreadlord.",
            "Garrosh did nothing wrong.",
            'Green Jesus says absolutely not.',
            "I DON'T KNOW!",
            "I'm not a fortunate teller."]

        random_answer = answers[random(0, len(answers)-1)]

        embed = discord.Embed(
            title=f'{ctx.author.display_name} has asked the magical 8Ball a question!',
            description=' ',
            colour=discord.Colour.purple())
        embed.set_thumbnail(url='https://i.imgur.com/J1eZMdt.png')
        embed.add_field(name=f'Question', value=f'{question}', inline=False)
        embed.add_field(name=f'Answer', value=f'{random_answer}', inline=False)
        embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'Brought to you by {self.bot.user.display_name} - {self.utils.get_time_parsed()}')
        await ctx.send(content=f'{ctx.author.mention}', embed=embed)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))