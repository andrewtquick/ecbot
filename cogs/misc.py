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
        await ctx.send(f'{ctx.author.mention} -> Here are some features Xylr is currently working on:\n```1. Item Price Lookup\n2. Item Lookup\n3. Mythic+ Guide Links\n4. Profession Guide Links\n```\nIf you think there is something that would be worth adding, please let Xylr know.''', delete_after=60)

    # Youtube Channel Command

    @Command(
        name='youtube',
        aliases=['yt'],
        help='Links the Elite Casuals Youtube Channel')
    async def youtube(self, ctx: Context):
        await ctx.send(f"{ctx.author.mention} -> Here is the Youtube link. https://www.youtube.com/channel/UCWeTRksGtMyXUd_Kn_f-svg")

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

    @Command(
        name='ranks',
        help='Displays the current DPS Ranks in raid')
    async def ranks(self, ctx: Context):
        await ctx.send(f"{ctx.author.mention} -> Here are the current DPS ranks.\nhttps://wow.zamimg.com/uploads/blog/images/23554-analysis-of-shadowlands-dps-in-mythic-castle-nathria-patch-9-0-5-week-of-april.png")

def setup(bot):
    bot.add_cog(Miscellaneous(bot))