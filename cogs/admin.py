import discord
import os
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

    # Kick Command

    @Command(
        name='kick',
        aliases=['k'],
        help='*Requires Admin* Kick a user from the server.',
        usage='@user <reason>')
    @commands.has_role('Guild Master')
    async def kick(self, ctx: Context, member: Member, *, reason='No reason given.'):
        officer_channel = self.bot.get_channel(self.OFFICER_CHANNEL)
        embed = self.embed_creator('kick', ctx.message.author.name, member.name, reason, ctx.message.author.avatar_url)
        await member.kick(reason=reason)
        await ctx.send(f'**{member.name}** has been kicked.')
        await officer_channel.send(embed=embed)

    # Ban command

    @Command(
        name='ban',
        aliases=['b'],
        help='*Requires Admin* Ban a user from the server.',
        usage='@user <reason>')
    @commands.has_role('Guild Master')
    async def ban(self, ctx: Context, member: Member, *, reason='No reason given.'):
        officer_channel = self.bot.get_channel(self.OFFICER_CHANNEL)
        embed = self.embed_creator('ban', ctx.message.author.name, member.name, reason, ctx.message.author.avatar_url)
        await member.ban(reason=reason)
        await ctx.send(f'**{member.name}** has been banned.')
        await officer_channel.send(embed=embed)

    # Mute Command

    @Command(
        name='mute',
        aliases=['m'],
        help='*Requires Admin* Mute a user in the voice channel.',
        usage='@user')
    @commands.has_role('Guild Master')
    async def mute(self, ctx: Context, member: Member, *, reason='No reason given.'):
        officer_channel = self.bot.get_channel(self.OFFICER_CHANNEL)
        embed = self.embed_creator('mute', ctx.message.author.name, member.name, reason, ctx.message.author.avatar_url)
        await member.edit(mute=True)
        await ctx.send(f'**{member.name}** has been muted.')
        await officer_channel.send(embed=embed)

    # Deafen Command

    @Command(
        name='deafen',
        aliases=['d'],
        help='*Requires Admin* Deafen a user in the voice channel.',
        usage='@user')
    @commands.has_role('Guild Master')
    async def deafen(self, ctx: Context, member: Member, *, reason='No reason given.'):
        officer_channel = self.bot.get_channel(self.OFFICER_CHANNEL)
        embed = self.embed_creator('deafen', ctx.message.author.name, member.name, reason, ctx.message.author.avatar_url)
        await member.edit(deafen=True)
        await ctx.send(f'**{member.name}** has been deafened.')
        await officer_channel.send(embed=embed)

    # Announcement Command

    @Command(
        name='announce',
        aliases=['a'],
        help='*Requires Admin* Send an announcement to the announcement channel.',
        usage='message')
    @commands.has_role('Guild Master')
    async def announce(self, ctx: Context, *, msg: str):
        announce_chan = self.bot.get_channel(self.ANNOUNCE_CHAN)
        await announce_chan.send(msg)

    # Embed Creator for Admin Commands

    def embed_creator(self, cmd, author, member, reason, avatar):

        embed = discord.Embed(
            title='Admin Command Used',
            description=f'{cmd.capitalize()} used by **{author}**',
            colour=discord.Colour.red())
        embed.set_thumbnail(url=avatar)
        embed.add_field(name=f'Reason', value=f'Reason: `{reason}`')
        embed.set_footer(text=f'Timestamp: {dt.now().ctime()}', icon_url=self.bot.user.avatar_url)
        return embed

def setup(bot):
    bot.add_cog(AdminControl(bot))