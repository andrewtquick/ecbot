import discord
from datetime import datetime as dt
from discord import Member as Member
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
        usage='@user <reason>'
        )
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
        usage='@user <reason>'
        )
    @commands.has_role('Admin')
    async def ban(self, ctx: Context, member: Member, *, reason='No reason given.'):
        officer_channel = self.bot.get_channel(self.OFFICER_CHANNEL)
        embed = self.embed_creator('ban', ctx.message.author.name, member.name, reason, ctx.message.author.avatar_url)
        await member.ban(reason=reason)
        await ctx.send(f'**{member.name}** has been banned.')
        await officer_channel.send(embed=embed)

    async def mute(self, member: Member):
        pass

    async def deafen(self, member: Member):
        pass

    async def link(self):
        pass

    async def annouce(self, ctx: Context):
        pass

    async def add_rank(self, member: Member):
        pass
    
    async def remove_rank(self, member: Member):
        pass

    def embed_creator(self, cmd, author, member, reason, avatar):

        if cmd == 'ban':
            message = 'has been banned from the server.'
        elif cmd == 'kick':
            message = 'has been kicked from the server.'
        elif cmd == 'mute':
            message = 'has been muted.'
        elif cmd == 'deafen':
            message = 'has been defeaned.'
        elif cmd == 'up_rank':
            message = 'has been promoted.'
        elif cmd == 'down_rank':
            message = 'has been demoted.'


        embed = discord.Embed(
            title='Admin Command Used',
            description=f'{cmd.capitalize()} used by **{author}**',
            colour=discord.Colour.red())
        embed.set_thumbnail(url=avatar)
        embed.add_field(name=f'Reason', value=f'Reason: `{reason}`')
        embed.add_field(name='Action', value=f'**{member}** {message}')
        embed.set_footer(text=f'Timestamp: {dt.now().ctime()}', icon_url=self.bot.user.avatar_url)
        return embed

def setup(bot):
    bot.add_cog(AdminControl(bot))