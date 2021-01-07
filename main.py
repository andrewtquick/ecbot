import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', description='Here is a list of available commands.\n To use the command, prefix the command with ".".', intents=intents)

exts = [
    'cogs.loadcog',
    'cogs.error_handler',
    'cogs.admin',
    'cogs.misc',
    'cogs.events'
]

if __name__ == '__main__':

    for ext in exts:
        bot.load_extension(ext)
    
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)