import discord
import os
from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix='.', description='Here is a list of available commands.\n To use the command, prefix the command with ".".', intents=discord.Intents().all())
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

exts = [
    'cogs.admin.admin',
    'cogs.events.events',
    'cogs.errors.error_handler',
    'cogs.misc.loadcog',
    'cogs.misc.misc',
    'cogs.warcraft.raids',
    'cogs.warcraft.gamble',
    'cogs.channel.channels',
    'cogs.misc.ec_commands'
]

if __name__ == '__main__':

    for ext in exts:
        bot.load_extension(ext)
    
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)