import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands import MissingRole, BadArgument, MissingPermissions, MissingAnyRole

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, err):
        if isinstance(err, MissingAnyRole):
            await ctx.send(f'Sorry {ctx.author.mention}, you do not have the permission to perform this command.', delete_after=20)

        print(err)

    
def setup(bot):
    bot.add_cog(ErrorHandler(bot))