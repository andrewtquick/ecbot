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
    'cogs.misc'
]

OFFICER_CHANNEL = int(os.getenv('OFFICER_CHANNEL'))
PURGATORY_CHAN = int(os.getenv('PURGATORY_CHAN'))

@bot.event
async def on_ready():
    print(f'{bot.user.name} online.')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='.help command'))

@bot.event
async def on_member_remove(member: discord.Member):
    ochannel = bot.get_channel(OFFICER_CHANNEL)
    await ochannel.send(f'**{member}** has left the server.')

@bot.event
async def on_member_join(member: discord.Member):
    ochannel = bot.get_channel(PURGATORY_CHAN)

    await ochannel.send(f'@Guild Master **{member.name}** has joined the server.')

    embed = discord.Embed(
        title="Welcome to Elite Casual's Discord Server",
        description='We are an AOTC focused raiding guild on Stormrage-US\n\u200b',
        colour=discord.Colour.blue())
    embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
    embed.add_field(name='📄 Server Rules', value='❌ No Racism\n❌ No Politics Discussion\n❌ No Toxicity\n❌ No NSFW Content\n✅ Have fun!\n\n**These rules are zero tolerance.**\n\u200b', inline=False)
    embed.add_field(name='👑 Guild Leadership', value='Xylr\nDiamondclaw\nZellah\n\u200b', inline=False)
    embed.add_field(name='❔ Looking to raid or just hang out?', value='Please be sure to reach out to the guild leadership with your intention.', inline=False)
    await member.send('https://i.imgur.com/gYeYMCM.png')
    await member.send(embed=embed)

if __name__ == '__main__':

    for ext in exts:
        bot.load_extension(ext)
    
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)