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
        help='Kick a user from the server. Must be Admin.',
        usage='@user <reason>')
    @commands.has_role('Admin')
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
        help='Ban a user from the server. Must be Admin.',
        usage='@user <reason>')
    @commands.has_role('Admin')
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
        help='Mute a user in the voice channel.',
        usage='@user')
    @commands.has_role('Admin')
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
        help='Deafen a user in the voice channel.',
        usage='@user')
    @commands.has_role('Admin')
    async def deafen(self, ctx: Context, member: Member, *, reason='No reason given.'):
        officer_channel = self.bot.get_channel(self.OFFICER_CHANNEL)
        embed = self.embed_creator('deafen', ctx.message.author.name, member.name, reason, ctx.message.author.avatar_url)
        await member.edit(deafen=True)
        await ctx.send(f'**{member.name}** has been deafened.')
        await officer_channel.send(embed=embed)

    # Invite Command

    @Command(
        name='invite',
        aliases=['i'],
        help='Generate an invite link to the text channel.',
        usage='<time limit in seconds> <max uses>')
    async def link(self, ctx: Context, limit=600, uses=0):
        inv_link = await ctx.channel.create_invite(max_age=limit, max_uses=uses, unique=True)
        if limit == 0 and uses == 0:
            await ctx.send(f'{ctx.author.mention} -> Here is your link.\n\n{inv_link}')
        else:
            m, s = divmod(float(limit), 60)
            if uses == 0:
                await ctx.send(f'{ctx.author.mention} -> Here is your link.\n\nRemember, the link is active for `{int(m)}m {int(s)}s`.\n\n{inv_link}')
            else:
                await ctx.send(f'{ctx.author.mention} -> Here is your link.\n\nRemember, the link is active for `{int(m)}m {int(s)}s` and can be used `{uses}` times.\n\n{inv_link}')

    # Announcement Command

    @Command(
        name='announce',
        aliases=['a'],
        help='Send an announcement to the announcement channel.',
        usage='message')
    @commands.has_role('Admin')
    async def announce(self, ctx: Context, *, msg: str):
        announce_chan = self.bot.get_channel(self.ANNOUNCE_CHAN)
        await announce_chan.send(msg)

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
            5. Class Guide Links
            6. Profession Guide Links
            7. WoW Token Price\n
            If you think there is something that would be worth adding, please let Xylr know.''')

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