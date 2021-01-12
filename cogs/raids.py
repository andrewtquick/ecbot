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

    # Castle Nathria Raid Guide Command

    @Command(
        name="nathria",
        aliases=['cn','nath','castle'],
        help="Displays raid boss specific information.")
    async def castle_nathria(self, ctx: Context, boss=None, difficulty=None):

        raid_bosses = {
            1 : "Shriekwing",
            2 : "Hunstman Altimor",
            3 : "Hungering Destroyer",
            4 : "Artificer Xy'Mox",
            5 : "Sun King's Salvation",
            6 : "Lady Inerva Darkvein",
            7 : "Council of Blood",
            8 : "Sludgefist",
            9 : "Stone Legion",
            10 : "Sire Denathrius"
        }

        raid_guides = {
            1 : {
                1 : 'https://mythictrap.com/castleNathria/shriekwing/normal/',
                2 : 'https://mythictrap.com/castleNathria/shriekwing/heroic/',
                3 : 'https://mythictrap.com/castleNathria/shriekwing/mythic'
            },
            2: {
                1 : 'https://mythictrap.com/castleNathria/altimor/normal/',
                2 : 'https://mythictrap.com/castleNathria/altimor/heroic/',
                3 : 'https://mythictrap.com/castleNathria/altimor/mythic/'
            },
            3: {
                1 : 'https://mythictrap.com/castleNathria/hungeringDestroyer/normal/',
                2 : 'https://mythictrap.com/castleNathria/hungeringDestroyer/heroic/',
                3 : 'https://mythictrap.com/castleNathria/hungeringDestroyer/mythic/'
            },
            4: {
                1 : 'https://mythictrap.com/castleNathria/artificerXyMox/normal/',
                2 : 'https://mythictrap.com/castleNathria/artificerXyMox/heroic/',
                3 : 'https://mythictrap.com/castleNathria/artificerXyMox/mythic/'
            },
            5: {
                1 : 'https://mythictrap.com/castleNathria/sunkingssalvation/normal/',
                2 : 'https://mythictrap.com/castleNathria/sunkingssalvation/heroic/',
                3 : 'https://mythictrap.com/castleNathria/sunkingssalvation/mythic/'
            },
            6: {
                1 : 'https://mythictrap.com/castleNathria/ladyInervaDarkvein/normal/',
                2 : 'https://mythictrap.com/castleNathria/ladyInervaDarkvein/heroic/',
                3 : 'https://mythictrap.com/castleNathria/ladyInervaDarkvein/mythic/'
            },
            7: {
                1 : 'https://mythictrap.com/castleNathria/theCouncilOfBlood/normal/',
                2 : 'https://mythictrap.com/castleNathria/theCouncilOfBlood/heroic/',
                3 : 'https://mythictrap.com/castleNathria/theCouncilOfBlood/mythic/'
            },
            8: {
                1 : 'https://mythictrap.com/castleNathria/sludgefist/normal/',
                2 : 'https://mythictrap.com/castleNathria/sludgefist/heroic/',
                3 : 'https://mythictrap.com/castleNathria/sludgefist/mythic/'
            },
            9: {
                1 : 'https://mythictrap.com/castleNathria/stoneLegionGenerals/normal/',
                2 : 'https://mythictrap.com/castleNathria/stoneLegionGenerals/herioc/',
                3 : 'https://mythictrap.com/castleNathria/stoneLegionGenerals/mythic/'
            },
            10: {
                1 : 'https://mythictrap.com/castleNathria/sireDenathrius/normal/',
                2 : 'https://mythictrap.com/castleNathria/sireDenathrius/heroic/',
                3 : 'https://mythictrap.com/castleNathria/sireDenathrius/mythic/'
            }}

        if boss == None:
            await ctx.send(f"{ctx.author.mention} Which boss would you like? Use the number next to the bosses name.\n```\n1 Shriekwing\n2 Huntsman Altimor\n3 Hungering Destroyer\n4 Artificer Xy'Mox\n5 Sun King's Salvation\n6 Lady Inerva Darkvein\n7 Council of Blood\n8 Sludgefist\n9 Stone Legion\n10 Sire Denathrius\n```", delete_after=20)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if int(msg.content) > 10 or int(msg.content) < 1:
                await ctx.send(f"**{ctx.author.mention}** -> Sorry, you selected something that doesn't exist. Please use `.cn` for a list of bosses.", delete_after=30)
                return
            else:
                boss = msg.content
                sel_boss = raid_bosses[int(boss)]
                if difficulty == None:
                    await ctx.send(f'{ctx.author.mention} -> You selected **{sel_boss}**. Now, which difficulty?\n```\n1 Normal\n2 Heroic\n3 Mythic\n```', delete_after=20)
                    msg_2 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

                    if int(msg_2.content) > 3 or int(msg_2.content) < 1:
                        await ctx.send(f"**{ctx.author.mention}** -> Sorry, you selected something that doesn't exist. Please use `.cn` for a list of bosses.", delete_after=30)
                    else:
                        diff = msg_2.content
                        sel_diff = raid_guides[int(boss)]

                        if diff == '1':
                            diff_name = 'Normal'
                        if diff == '2':
                            diff_name = 'Heroic'
                        if diff == '3':
                            diff_name = 'Mythic'

                        await ctx.send(f'**{ctx.author.mention}** -> Great! Here is the **{diff_name}** Guide for **{sel_boss}**. - {sel_diff[int(diff)]}', delete_after=60)
                        return   
        else:
            if difficulty == None:
                await ctx.send(f'{ctx.author.mention} -> You selected **{raid_bosses[int(boss)]}**. Now, which difficulty?\n```\n1 Normal\n2 Heroic\n3 Mythic\n```', delete_after=20)
                msg_2 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

                if int(msg_2.content) > 3 or int(msg_2.content) < 1:
                    await ctx.send(f"**{ctx.author.mention}** -> Sorry, you selected something that doesn't exist. Please use `.cn` for a list of bosses.", delete_after=30)
                    return
                else:
                    diff = msg_2.content
                    sel_diff = raid_guides[int(boss)]

                    if diff == '1':
                        diff_name = 'Normal'
                    if diff == '2':
                        diff_name = 'Heroic'
                    if diff == '3':
                        diff_name = 'Mythic'

                    await ctx.send(f'**{ctx.author.mention}** -> Great! Here is the **{diff_name}** Guide for **{raid_bosses[int(boss)]}**. - {sel_diff[int(diff)]}', delete_after=60)
                    return

        if int(boss) > 10 or int(difficulty) > 3 or int(boss) < 1 or int(difficulty) < 1:
            await ctx.send(f"**{ctx.author.mention}** -> Sorry, you selected something that doesn't exist. Please use `.cn` for a list of bosses.", delete_after=30)
            return
        else:
            if difficulty == '1':
                diff_name = 'Normal'
            if difficulty == '2':
                diff_name = 'Heroic'
            if difficulty == '3':
                diff_name = 'Mythic'

            sel_diff = raid_guides[int(boss)]
            await ctx.send(f'**{ctx.author.mention}** -> Here is the **{diff_name}** Guide for **{raid_bosses[int(boss)]}**. - {sel_diff[int(difficulty)]}', delete_after=60)

def setup(bot):
    bot.add_cog(Raids(bot))