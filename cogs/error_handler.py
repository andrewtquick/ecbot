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
            await ctx.send(f'Sorry {ctx.author.mention}, you do not have the permission to perform this command.')

        print(type(err))
    
def setup(bot):
    bot.add_cog(ErrorHandler(bot))