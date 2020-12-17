import discord
from datetime import datetime as dt
from discord import Member
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context

class AdminControl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.OFFICER_CHANNEL = 785518643312066570

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

    @Command(
        name='invite',
        aliases=['i'],
        help='Generate an invite link to the text channel.',
        usage='<time limit in seconds> <max uses>')
    async def link(self, ctx: Context, *arg):
        limit, uses = arg
        m, s = divmod(float(limit), 60)
        inv_link = await ctx.channel.create_invite(max_age=limit, max_uses=uses, unique=True)
        await ctx.send(f'{ctx.author.mention} -> Here is your link.\n\nRemember, the link is active for `{int(m)}m {int(s)}s` and can be used `{uses}` times.')
        await ctx.send(inv_link)

    async def annouce(self, ctx: Context):
        pass

    async def add_rank(self, member: Member):
        pass
    
    async def remove_rank(self, member: Member):
        pass

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