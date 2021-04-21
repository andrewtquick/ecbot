import discord
import os
import requests
from discord import Member
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context

class ServerStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    


def setup(bot):
    bot.add_cog(ServerStatus(bot))