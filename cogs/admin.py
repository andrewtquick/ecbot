import discord
import os
import pytz
from datetime import datetime as dt
from discord import Member
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context
from misc.firebase import DBConnection
from misc.utils import Utils
from firebase_admin import db

class AdminControl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.OFFICER_CHANNEL = os.getenv('OFFICER_CHANNEL')
        self.ANNOUNCE_CHAN = os.getenv('ANNOUNCE_CHAN')
        self.AMONG_US_CHAN = os.getenv('AMOUNG_US_CHAN')
        self.tz = pytz.timezone('America/New_York')
        self.utils = Utils(self)
        self.ecdb = DBConnection(self)

    # Kick Command

    @Command(
        name='kick',
        aliases=['k'],
        help='*Requires Admin* Kick a user from the server.',
        usage='@user')
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def kick(self, ctx: Context, member: Member):
        await member.kick()

    # Ban command

    @Command(
        name='ban',
        aliases=['b'],
        help='*Requires Admin* Ban a user from the server.',
        usage='@user <reason>')
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def ban(self, ctx: Context, member: Member, *, reason='No reason given.'):
        await member.ban(reason=reason)

    # Mute Command

    @Command(
        name='mute',
        aliases=['m'],
        help='*Requires Admin* Mute a user in the voice channel.',
        usage='@user')
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def mute(self, ctx: Context, member: Member, *, reason='No reason given.'):
        await member.edit(mute=True)

    # Mute All Command

    @Command(
        name='muteall',
        aliases=['ma'],
        help='*Requires Admin* Mute all users in a voice channel.',
        usage='<channel id>')
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def mute_all(self, ctx: Context, chan=None):
        if chan == None:
            await ctx.send(f'{ctx.author.mention} -> You must specify a voice channel. Use .help ma for assistance.')
        else:
            channel = self.bot.get_channel(int(chan))
            members = channel.members

            for member in members:
                await member.edit(mute=True)

    # Un-Mute All Command

    @Command(
        name='unmuteall',
        aliases=['uma'],
        help="*Requires Admin* Un-Mute all users in a voice channel.",
        usage="<channel id>")
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def unmute_all(self, ctx: Context, chan=None):
        if chan == None:
            await ctx.send(f'{ctx.author.mention} -> You must specify a voicc channel. Use .help uma for assistance.')
        else:
            channel = self.bot.get_channel(int(chan))
            members = channel.members

            for member in members:
                await member.edit(mute=False)

    # Squelch Command

    @Command(
        name='squelch',
        aliases=['s'],
        help='*Requires Admin* Deafens and Mutes all users in a voice channel.',
        usage="<channel id>")
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def squelch(self, ctx: Context, chan=None):
        if chan == None:
            channel = self.bot.get_channel(int(self.AMONG_US_CHAN))
            members = channel.members

            for member in members:
                await member.edit(mute=True, deafen=True)

        else:
            channel = self.bot.get_channel(int(chan))
            members = channel.members

            for member in members:
                await member.edit(mute=True, deafen=True)

    # Unsquelch Command

    @Command(
        name='unsquelch',
        aliases=['us'],
        help='*Requires Admin* Deafens and Mutes all users in a voice channel.',
        usage="<channel id>")
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def unsquelch(self, ctx: Context, chan=None):
        if chan == None:
            channel = self.bot.get_channel(int(self.AMONG_US_CHAN))
            members = channel.members

            for member in members:
                await member.edit(mute=False, deafen=False)
                
        else:
            channel = self.bot.get_channel(int(chan))
            members = channel.members

            for member in members:
                await member.edit(mute=False, deafen=False)

    # Deafen Command

    @Command(
        name='deafen',
        aliases=['d'],
        help='*Requires Admin* Deafen a user in the voice channel.',
        usage='@user')
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def deafen(self, ctx: Context, member: Member, *, reason='No reason given.'):
        await member.edit(deafen=True)
 
    # Announcement Command

    @Command(
        name='announce',
        aliases=['a'],
        help='*Requires Admin* Send an announcement to the announcement channel.',
        usage='message')
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def announce(self, ctx: Context, *, msg: str):
        announce_chan = self.bot.get_channel(int(self.ANNOUNCE_CHAN))
        await announce_chan.send(msg)

    # Friends and Family Command

    @Command(
        name='friend',
        aliases=['ff'],
        help='Adds the Friends and Family role to a user.',
        usage='@user')
    async def friends_family(self, ctx: Context, member: Member):
        role = discord.utils.get(ctx.guild.roles, name='Friends and Family')
        ochannel = self.bot.get_channel(int(self.OFFICER_CHANNEL))
             
        if role in member.roles:
            await ctx.send(f'{ctx.author.mention} -> **{member.name}** already has that role.', delete_after=60)
        else:
            await member.add_roles(role, atomic=True)
            await ctx.send(f'{ctx.author.mention} -> Added `Friends and Family` rank to **{member.name}**', delete_after=60)
            await ochannel.send(f"**{ctx.author.name}** added the `Friends and Family` rank to **{member.name}**. `Timestamp: {dt.now(self.tz).strftime('%x %X')}`")

    # Rules Command

    @Command(
        name='rules',
        aliases=['gr'],
        help='Displays the Guild and Discord Rules.')
    async def guild_rules(self, ctx: Context):
        await ctx.send(f'{ctx.author.mention}\n```📄 Server Rules 📄\n\n❌ No Racism\n❌ No Politics Discussion\n❌ No Toxicity\n❌ No NSFW Content\n✅ Have fun!```\n**These rules are zero tolerance.**')

    # Leadership Command

    @Command(
        name='leadership',
        aliases=['gl'],
        help='Displays the Guild and Discord Leadership')
    async def leadership(self, ctx: Context):
        await ctx.send(f'{ctx.author.mention}\n```👑 Guild Leadership 👑\n\nXylr\nDiamondclaw\nZellah\n\nGuild Advisor:\nJaemyst\nFuzzybottomz```')

    # Who reacted to message

    @Command(
        name='who reacted',
        aliases=['wr'],
        help='Displays who responded to specific message, by id',
        usage='message_id')
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def who_reacted(self, ctx: Context, msg: int):
        chan = self.bot.get_channel(int(self.ANNOUNCE_CHAN))
        message_id = await chan.fetch_message(msg)
        users = set()

        for reaction in message_id.reactions:
            async for user in reaction.users():
                users.add(user)

        await ctx.send(f"{ctx.author.mention} -> Here is the list of users that responded:\n {', '.join(user.name for user in users)}")

    # Whois command

    @Command(
        name='whois',
        help='Displays information about a user',
        usage='user')
    @commands.has_any_role('Admin', 'Guild Master', 'Guild Advisor')
    async def whois(self, ctx: Context, member: Member):
        user_ref = db.reference('users')
        user_check = user_ref.child(str(member.id))
        ret_data = user_check.get()
        nicknames = []

        embed = discord.Embed(
            title=f'Whois information for {member.display_name}',
            description=f'Here is all the information I found for **{member.display_name}**',
            colour=discord.Colour.orange())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Member Name', value=ret_data['member'], inline=False)
        embed.add_field(name='Display Name', value=ret_data['member_name'], inline=False)
        embed.add_field(name='Joined Date', value=ret_data['joined_at'], inline=False)

        if 'nickname' in ret_data:
            for k,v in ret_data.items():
                if k == 'nickname':
                    nicknames.append(v)
            embed.add_field(name='Nicknames', value=', '.join(name for name in nicknames), inline=False)

        if 'self_leave' in ret_data:
            left_date = self.utils.parse_date_time(str(ret_data['self_leave']))
            embed.add_field(name='Date and time user left', value=left_date)

        await ctx.send(f'{ctx.author.mention}', embed=embed)

def setup(bot):
    bot.add_cog(AdminControl(bot))