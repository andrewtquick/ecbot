import discord
import os
from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(
    command_prefix='.',
    intents=discord.Intents().all(),
    help_command=None)

slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

exts = [
    'cogs.admin.admin',
    'cogs.events.events',
    'cogs.errors.error_handler',
    'cogs.general.loadcog',
    'cogs.general.misc',
    'cogs.general.ec_commands',
    'cogs.general.help',
    'cogs.warcraft.raids',
    'cogs.warcraft.gamble',
    'cogs.warcraft.dungeons',
]

if __name__ == '__main__':

    for ext in exts:
        bot.load_extension(ext)
    
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)