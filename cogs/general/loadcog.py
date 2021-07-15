import discord
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context

class CogControl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @Command(name='load', hidden=True, aliases=['l'])
    @commands.check_any(commands.is_owner())
    @commands.guild_only()
    async def load_cog(self, ctx: Context, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as err:
            await ctx.send(f'{ctx.author.mention} -> **`### ERROR ###`**: {type(err).__name__} - {err}')
        else:
            await ctx.send(f'{ctx.author.mention} -> **`### SUCCESS ###`** {cog} has been loaded.', delete_after=10)

    @Command(name='unload', hidden=True, aliases=['u'])
    @commands.check_any(commands.is_owner())
    @commands.guild_only()
    async def unload_cog(self, ctx: Context, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as err:
            await ctx.send(f'{ctx.author.mention} -> **`### ERROR ###`**: {type(err).__name__} - {err}')
        else:
            await ctx.send(f'{ctx.author.mention} -> **`### SUCCESS ###`** {cog} has been unloaded.', delete_after=10)

    @Command(name='reload', hidden=True, aliases=['r'])
    @commands.check_any(commands.is_owner())
    @commands.guild_only()
    async def reload_cog(self, ctx: Context, *, cog: str):

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as err:
            await ctx.send(f'{ctx.author.mention} -> **`### ERROR ###`**: {type(err).__name__} - {err}')
        else:
            await ctx.send(f'{ctx.author.mention} -> **`### SUCCESS ###`** {cog} has been reloaded.', delete_after=10)

    @Command(name='cogs', hidden=True, aliases=['c'])
    @commands.check_any(commands.is_owner())
    @commands.guild_only()
    async def list_cogs(self, ctx: Context):
        cogs = self.bot.extensions.keys()
        cog_name = ', '.join(cogs)
        await ctx.send(f"{ctx.author.mention} Currently loaded cogs: **`{cog_name}`**", delete_after=10)

def setup(bot):
    bot.add_cog(CogControl(bot))
