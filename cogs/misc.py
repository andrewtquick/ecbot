import discord
import os
import requests
from discord import Member
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.CLIENT_ID = os.getenv('WOW_API')
        self.CLIENT_SECRET = os.getenv('API_SECRET')

    # Invite Command

    @Command(
        name='invite',
        aliases=['i'],
        help='Generate an invite link to the server.',
        usage='<time limit in seconds> <max uses>')
    async def link(self, ctx: Context, limit=600, uses=0):
        inv_link = await ctx.channel.create_invite(max_age=limit, max_uses=uses, unique=True)
        if limit == 0 and uses == 0:
            await ctx.send(f'{ctx.author.mention} -> Here is your link.\n\n{inv_link}', delete_after=60)
        else:
            m, s = divmod(float(limit), 60)
            if uses == 0:
                await ctx.send(f'{ctx.author.mention} -> Here is your link.\n\nRemember, the link is active for `{int(m)}m {int(s)}s`.\n\n{inv_link}', delete_after=60)
            else:
                await ctx.send(f'{ctx.author.mention} -> Here is your link.\n\nRemember, the link is active for `{int(m)}m {int(s)}s` and can be used `{uses}` times.\n\n{inv_link}', delete_after=60)

     # Elite Casuals Guild Logo Command

    @Command(
        name='logo',
        help="Links the Elite Casual's logo")
    async def logo(self, ctx: Context):
        await ctx.send(f'{ctx.author.mention} -> Here you are!\nhttps://i.imgur.com/gYeYMCM.png')

    # Feature Command

    @Command(
        name='features',
        aliases=['f'],
        help='List of upcoming features for EC Bot')
    async def features(self, ctx: Context):
        await ctx.send(
            f'''{ctx.author.mention} -> Here are some features Xylr is currently working on:\n
            1. Item Price Lookup
            2. Item Lookup
            3. Raid Guide Links
            4. Mythic+ Guide Links
            5. Profession Guide Links
            If you think there is something that would be worth adding, please let Xylr know.''', delete_after=60)

    # WoW Token Price Getter

    @Command(
        name='wowtoken',
        aliases=['wt'],
        help='Fetches the current WoW Token price.')
    async def wow_token(self, ctx: Context):
        grant = self.blizzard_access_token()
        resp = requests.get('https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US&access_token=%s' % grant).json()
        price = str(resp['price'])[:-4]
        price = [i for i in price]
        price.insert(3,',')
        await ctx.send(f"{ctx.author.mention} -> **WoW Token Price is currently:** `{''.join(price)}g`")

    # Method for grabbing access token to Blizzard API

    def blizzard_access_token(self):
        data = { 'grant_type' : 'client_credentials' }
        resp = requests.post('https://us.battle.net/oauth/token', data=data, auth=(self.CLIENT_ID, self.CLIENT_SECRET)).json()
        return resp['access_token']

def setup(bot):
    bot.add_cog(Miscellaneous(bot))