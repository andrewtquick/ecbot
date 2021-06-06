import discord
import os
import pytz
from datetime import datetime as dt
from discord import Member
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context

class AdminControl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.OFFICER_CHANNEL = os.getenv('OFFICER_CHANNEL')
        self.ANNOUNCE_CHAN = os.getenv('ANNOUNCE_CHAN')
        self.AMONG_US_CHAN = os.getenv('AMOUNG_US_CHAN')
        self.tz = pytz.timezone('America/New_York')

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

def setup(bot):
    bot.add_cog(AdminControl(bot))