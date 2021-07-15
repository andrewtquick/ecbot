import discord
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context, group, CommandInvokeError
from misc.firebase import DBConnection
from misc.utils import Utils
from firebase_admin import db

class ChannelAdmin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = DBConnection()
        self.utils = Utils(self)

    # Set channel command

    @group(
        name='setchan',
        help='Set specific channels for bot events',
        invoke_without_command=True,
        usage='<channel type> [channel name or id]')
    @commands.has_permissions(administrator=True)
    async def set_chan(self, ctx: Context):

        cmd = self.bot.get_command('setchan')
        channels = []

        if isinstance(cmd, commands.Group):
            for subcmd in cmd.walk_commands():
                channels.append(subcmd.name)
        
        chans = ' \n'.join(chan for chan in channels)
        await ctx.send(f'{ctx.author.mention} -> Here is a list of channels you can set for specific `{self.bot.user.display_name}` events.\n```{chans}```')

    # Set Announcement channel subcommand

    @set_chan.command(
        name='announce',
        help='Set channel for the announcements',
        usage='<channel name or id>')
    async def set_announce_chan(self, ctx: Context, chan):
        set_chan = self.set_channel('announce', ctx, chan)

        if set_chan:
            await ctx.send(f'{ctx.author.mention} -> Setting `#{set_chan}` for announcements.')
        else:
            raise CommandInvokeError('No such channel')

    # Set Admin channel subcommand

    @set_chan.command(
        name='admin',
        help='Set channel for admin event information.',
        usage='<channel name or id>')
    async def set_admin_chan(self, ctx: Context, chan):
        set_chan = self.set_channel('admin', ctx, chan)

        if set_chan:
            await ctx.send(f'{ctx.author.mention} -> Setting `#{set_chan}` for admin events.')
        else:
            raise CommandInvokeError('No such channel')

    # Set event channel subcommand

    @set_chan.command(
        name='event',
        help='Set channel for events command.',
        usage='<channel name or id>')
    async def set_event_chan(self, ctx: Context, chan):
        set_chan = self.set_channel('event', ctx, chan)

        if set_chan:
            await ctx.send(f'{ctx.author.mention} -> Setting `#{set_chan}` for events.')
        else:
            raise CommandInvokeError('No such channel')

    # Set WoW Gold gambling channel subcommand

    @set_chan.command(
        name='gamble',
        help='Set WoW gambling channel.',
        usage='<channel name or id>')
    async def set_gamble_chan(self, ctx: Context, chan):
        set_chan = self.set_channel('gamble', ctx, chan)

        if set_chan:
            await ctx.send(f'{ctx.author.mention} -> Setting `#{set_chan}` for WoW gold gambling.')
        else:
            raise CommandInvokeError('No such channel')

    # Channel setter to database

    def set_channel(self, cmd, ctx: Context, chan):
        check_chan = self.utils.channel_parse(chan)
        
        if check_chan == False:
            try:
                get_chan = discord.utils.get(ctx.guild.channels, name=chan, type=discord.ChannelType.text)
                set_chan = self.db.ecdb.child(str(ctx.guild.id)).child('channels')
                set_chan.update({cmd: str(get_chan.id)})
                return chan
            except Exception:
                return False
        else:
            get_chan = self.bot.get_channel(int(chan))
            if isinstance(get_chan, discord.channel.TextChannel):
                set_chan = self.db.ecdb.child(str(ctx.guild.id)).child('channels')
                set_chan.update({str(cmd): str(chan)})
                return get_chan.name
            else:
                return False

    # Catching raised exception

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send(f"{ctx.author.mention} -> I'm unable to find that text channel. Please double check the spelling or channel id.")

def setup(bot):
    bot.add_cog(ChannelAdmin(bot))