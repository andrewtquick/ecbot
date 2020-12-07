import discord
import os
from discord.ext import commands

# https://discord.com/api/oauth2/authorize?client_id=782672278365667329&scope=bot&permissions=8

bot = commands.Bot(command_prefix='.', description='Here is a list of available commands.\n To use the command, prefix the command with ".".')

exts = [
    'cogs.loadcog',
    'cogs.error_handler',
    'cogs.admin'
]

@bot.event
async def on_ready():
    print(f'{bot.user.name} online.')

@bot.event
async def on_member_leave(member: discord.Member):
    officer_channel = bot.get_channel(785518643312066570)
    await officer_channel.send(f'**{member}** has left the server.')

@bot.event
async def on_member_join(member: discord.Member):
    officer_channel = bot.get_channel(785518643312066570)
    await officer_channel.send(f'**{member}** has joined the server. They can only see the `#general` channel until you assign them a role.')

if __name__ == '__main__':

    for ext in exts:
        bot.load_extension(ext)
    
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)