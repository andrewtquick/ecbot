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
        self.tz = pytz.timezone('America/New_York')

    # Kick Command

    @Command(
        name='kick',
        aliases=['k'],
        help='*Requires Admin* Kick a user from the server.',
        usage='@user')
    @commands.has_any_role('Admin', 'Guild Master', 'Raid Lead')
    async def kick(self, ctx: Context, member: Member):
        await member.kick()

    # Ban command

    @Command(
        name='ban',
        aliases=['b'],
        help='*Requires Admin* Ban a user from the server.',
        usage='@user <reason>')
    @commands.has_any_role('Admin', 'Guild Master', 'Raid Lead')
    async def ban(self, ctx: Context, member: Member, *, reason='No reason given.'):
        await member.ban(reason=reason)

    # Mute Command

    @Command(
        name='mute',
        aliases=['m'],
        help='*Requires Admin* Mute a user in the voice channel.',
        usage='@user')
    @commands.has_any_role('Admin', 'Guild Master', 'Raid Lead')
    async def mute(self, ctx: Context, member: Member, *, reason='No reason given.'):
        await member.edit(mute=True)

    # Deafen Command

    @Command(
        name='deafen',
        aliases=['d'],
        help='*Requires Admin* Deafen a user in the voice channel.',
        usage='@user')
    @commands.has_any_role('Admin', 'Guild Master', 'Raid Lead')
    async def deafen(self, ctx: Context, member: Member, *, reason='No reason given.'):
        await member.edit(deafen=True)
 
    # Announcement Command

    @Command(
        name='announce',
        aliases=['a'],
        help='*Requires Admin* Send an announcement to the announcement channel.',
        usage='message')
    @commands.has_any_role('Admin', 'Guild Master', 'Raid Lead')
    async def announce(self, ctx: Context, *, msg: str):
        announce_chan = self.bot.get_channel(int(self.ANNOUNCE_CHAN))
        await announce_chan.send(msg)

    # Friends and Family Command

    @Command(
        name='friend',
        aliases=['ff'],
        help='Adds the Friends and Family role to a user.',
        usage='@user')
    @commands.has_any_role('Admin', 'Guild Master', 'Elite', 'Mythic+')
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
        await ctx.send(f'{ctx.author.mention}\n```👑 Guild Leadership 👑\n\nXylr (Reidx)\nDiamondclaw\nZellah\n\nRaid Lead:\nNock the Block```')

def setup(bot):
    bot.add_cog(AdminControl(bot))