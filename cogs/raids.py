import discord
import os
import requests
from discord import Member
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context

class Raids(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @Command(
        name="nathria",
        aliases=['cn','nath','castle'],
        help="Displays raid boss specific information.",
        usage="shriek normal\n.cn hunts heroic\n.castle sire mythic")
    async def castle_nathria(self, ctx: Context, boss=None, difficulty=None):
        
        if boss == None:
            await ctx.send(
                '''Which boss?
                Shriekwing
                Huntsman Altimor
                Hungering Destroyer
                Artificer Xy'Mox
                Sun King's Salvation
                Lady Inerva Darkvein
                Council of Blood
                Sludgefist
                Stone Legion
                Sire Denathrius
                ''', delete_after=10)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            boss = msg.content.lower()
        
            if difficulty == None:
                await ctx.send(
                    '''Which difficulty?
                    Normal
                    Heroic
                    Mythic
                    ''', delete_after=10)
                msg_2 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

                if msg_2.content.lower() == 'normal' and boss == 'shriek':
                    await ctx.send(f'**{ctx.author.mention}** -> Here is the Normal Guide for {self.format_boss_name(boss)}.\nhttps://mythictrap.com/castleNathria/shriekwing/normal/')

    

    def format_boss_name(self, boss):

        if boss == 'shriek':
            return 'Shriekwing'
        if boss == 'sw':
            return 'Shriekwing'
        if boss == 'hunts':
            return 'Huntsman Altimor'
        if boss == 'ha':
            return 'Huntsman Altimor'
        if boss == 'huntsman':
            return 'Huntsman Altimor'

        


def setup(bot):
    bot.add_cog(Raids(bot))