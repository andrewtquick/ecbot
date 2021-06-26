import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands import MissingRole, BadArgument

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, err):

        if isinstance(err, MissingRole):
            await ctx.send(f'Sorry {ctx.author.mention}, you do not have the permission to perform this command.', delete_after=20)

        if isinstance(err, BadArgument):
            await ctx.send(f"{ctx.author.mention} -> Sorry, not sure who that is. Please ensure you spelled the user's name correctly.", delete_after=20)

    
def setup(bot):
    bot.add_cog(ErrorHandler(bot))