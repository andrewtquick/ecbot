import discord
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context
from misc.firebase import DBConnection
from misc.utils import Utils

class CustomHelpCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ecdb = DBConnection()
        self.utils = Utils(self)
        self.prefix = '.'

    # Custom Help Command

    @Command(name='help', help='Displays the help command', usage='<command>')
    async def help_cmd(self, ctx: Context, cmd=None, tertiary=None):

        if ctx.author.guild_permissions.administrator:
            bot_cmds = self.bot.commands
            cmds = self.get_cmds()
            maxlen = self.get_max_len(cmds)
            cmd_dict = self.create_dict(bot_cmds, maxlen)
            cmd_list = '\n'.join('{} {}'.format(*i) for i in sorted(cmd_dict.items()))
            if cmd == None:
                await ctx.send(f'{ctx.author.mention}\n```Here is a list of available Admin Commands.\nPlease insure you prefix the command with a "ec."\n\nCommands:\n{cmd_list}\n\nFor additional help, you use {self.prefix}help <command>```')
            else:

                requested_cmd = self.bot.get_command(cmd)
                if tertiary:

                    if isinstance(requested_cmd, commands.Group):
                        cmd_help = ''
                        for subcmd in requested_cmd.walk_commands():
                            if tertiary in subcmd.name:
                                cmd_help = f'{self.prefix}{cmd} {subcmd.name} {subcmd.usage}\n\n{subcmd.help}'
                        await ctx.send(f"{ctx.author.mention}```{cmd_help}```")
                    else:
                        if requested_cmd:
                            await ctx.send(f"{ctx.author.mention}\n```{self.prefix}{requested_cmd.name} {requested_cmd.usage}\n\n{requested_cmd.help}```")
                        else:
                            await ctx.send(f"{ctx.author.mention} -> Sorry, I don't recognize that command. Please double check the spelling, or use `{self.prefix}help` for more information.")
                else:
                    await ctx.send(f"{ctx.author.mention}\n```{self.prefix}{requested_cmd.name} {requested_cmd.usage}\n\n{requested_cmd.help}```")

        else:
            embed = discord.Embed(
                title='Bot Commands have been changed!',
                description="All commands are now slash commands. Details below.\n\u200b",
                colour=discord.Colour.blurple())
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.add_field(
                name='Slash Commands',
                value=f"I used to respond to commands that were prefixed a specific way. However, that has been changed to slash commands. To use a command, just type a / in the chat window, and you'll see a list of commands that are available!\n\nWhen you type the slash, look for my name and you'll see which commands are available.")
            embed.set_footer(icon_url=self.bot.user.avatar_url, text=f'Brought to you by {self.bot.user.display_name} - {self.utils.get_time_parsed()}')
            await ctx.send(f'{ctx.author.mention}', embed=embed)

    # Getting command name

    def get_cmds(self):
        return [command.name for command in self.bot.commands if not command.hidden]

    # Finding command name with longest length

    def get_max_len(self, cmdlist):
        return len(max(cmdlist, key=len))

    # Creating a dictionary concatenating the command and help info

    def create_dict(self, cmds, maxlen):
        return {command.name.ljust(maxlen): command.help for command in cmds if not command.hidden}

def setup(bot):
    bot.add_cog(CustomHelpCommand(bot))