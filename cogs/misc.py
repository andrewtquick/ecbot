import discord
import os
import requests
from random import randint as random
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

    # Twitch TV Command

    @Command(
        name='twitch',
        aliases=['ttv'],
        help="Links to Xylr's Live Twitch Stream")
    async def twitch(self, ctx: Context):
        await ctx.send(f"{ctx.author.mention} -> Here is Xylr's Stream. http://www.twitch.tv/xylr")

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

    # Ranks Command

    @Command(
        name='ranks',
        help='Displays the current DPS Ranks in raid')
    async def ranks(self, ctx: Context):
        await ctx.send(f"{ctx.author.mention} -> Here are the current DPS ranks.\nhttps://wow.zamimg.com/uploads/blog/images/23554-analysis-of-shadowlands-dps-in-mythic-castle-nathria-patch-9-0-5-week-of-april.png")

    # 8-ball Command

    @Command(
        name='8ball',
        help='Ask the 8Ball a question')
    async def eight_ball(self, ctx: Context, msg=''):

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
            "I'm not a fortunate teller.",
            "https://imgur.com/a/EklZPAu"]

        no_message = [
            'Hey dingbat, you have to ask me a question.',
            'Stop wasting my time, ask me a question after the command.',
            'Well, what was your question, nerd.',
            'I think you forgot something, try .help 8ball',
            "HEY, YOU DIDN'T ASK ME A QUESTION.",
            'Want to try that again?',
            "Bruh, I can't read minds. Next time ask me your question."]

        if not msg:
            random_answer = no_message[random(0, len(no_message)-1)]
            await ctx.send(f'{ctx.author.mention} :: {random_answer}')
        else:
            random_answer = answers[random(0, len(no_message)-1)]
            await ctx.send(f'{ctx.author.mention} :: {random_answer}')

def setup(bot):
    bot.add_cog(Miscellaneous(bot))