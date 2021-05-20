import discord
import os
from random import randint as Random
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context


class Gamble(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.GAMBLE_CHAN = os.getenv('GAMBLE_CHAN')
        self.active_game = False
        self.gamble_amount = 0
        self.gamblers = []
        self.gamblers_rolled = {}
        self.game_creator = None
        self.auto_roll = True

    # Gambling Game Starter Command

    @Command(name='gamble', aliases=['g'], help='To start a game, type .gamble <amount> <on|off>. Auto Roll is on by default.')
    async def start_game(self, ctx: Context, amount: int, auto_roll='on'):

        gamble_chan = self.bot.get_channel(int(self.GAMBLE_CHAN))

        if ctx.channel == gamble_chan:
            if self.active_game == False:
                self.active_game = True
                self.gamble_amount = amount
                self.game_creator = ctx.author.name
                
                if auto_roll.lower() == 'off':
                    self.auto_roll = False

                embed = discord.Embed(title="World of Warcraft Gold Gambling has started!", description=f'HiLo roll for **{self.gamble_amount}<:goldcoin:844724052294893568>**. Started by **{self.game_creator}**', colour=discord.Colour.orange())
                embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
                embed.add_field(name='🟢 Entry', value='To **join**, click ✅\nTo **leave**, click ❌', inline=False)
                embed.add_field(name='📄 Rules', value='1. You must pay in game at your earliest convenience!\n2. Have fun and be respectful!', inline=False)
                embed.add_field(name='🛠️ Instructions', value='**Only the game starter can use the commands below**\nClick 🎲 to start the game\nClick 🗑️ to cancel the game', inline=False)
                embed.add_field(name='Current Gamblers', value='None', inline=False)
                
                msg = await ctx.send(embed=embed)
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                await msg.add_reaction('🎲')
                await msg.add_reaction('🗑️')

            else:
                await ctx.send(f'{ctx.author.mention} -> There is already an active game. Use command .current for more information', delete_after=10)
        else:
            await ctx.send(f'{ctx.author.mention} -> Sorry, gambling is only available in the #gambling channel.', delete_after=10)

    # Monitoring for reaction adds - should move to events file at some point

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.bot:
            return

        if payload.channel_id == int(self.GAMBLE_CHAN):
            chan = self.bot.get_channel(payload.channel_id)
            msg = await chan.fetch_message(payload.message_id)
            embed = msg.embeds[0]

            if payload.emoji.name == '🗑️' and payload.member.name == self.game_creator:
                self.active_game = False
                cancel_embed = discord.Embed(title="World of Warcraft Gold Gambling has been cancelled!", description=f'Cancelled by **{self.game_creator}**', colour=discord.Colour.orange())
                cancel_embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
                cancel_embed.add_field(name='❌ Cancelled', value='Gamble entry has been cancelled.', inline=False)
                await msg.edit(embed=cancel_embed, delete_after=10)
                await msg.clear_reactions()

            elif payload.emoji.name == '🎲' and payload.member.name == self.game_creator and len(self.gamblers) >= 2:
                self.active_game = False
                await msg.clear_reactions()
                roll_embed = discord.Embed(title='World of Warcraft Gold Gambling: Rolling has begun!', description=f'Rolling started by **{self.game_creator}**', colour=discord.Colour.orange())
                roll_embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
                roll_embed.add_field(name=f'Gambling', value=f'{self.gamble_amount}g', inline=False)
                roll_embed.add_field(name='Begin Rolling', value='No more entries allowed. Begin rolling with .roll', inline=False)
                roll_embed.add_field(name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)
                await msg.edit(embed=roll_embed)
                
                await self.begin_roll()

            else:

                if payload.emoji.name == '✅':
                    embed_dict = embed.to_dict()
                    if not payload.member.name in embed_dict['fields'][3]['value']:
                        if 'None' in self.gamblers:
                            self.gamblers.remove('None')
                            self.gamblers.append(payload.member.name)
                            embed.set_field_at(3, name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)
                        else:
                            self.gamblers.append(payload.member.name)
                            embed.set_field_at(3, name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)

                if payload.emoji.name == '❌':
                    embed_dict = embed.to_dict()
                    if payload.member.name in embed_dict['fields'][3]['value']:
                        self.gamblers.remove(payload.member.name)
                        if len(self.gamblers) == 0:
                            self.gamblers.append('None')
                            embed.set_field_at(3, name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)
                        else:
                            embed.set_field_at(3, name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)


                await msg.edit(embed=embed)
                await msg.remove_reaction(payload.emoji, payload.member)

                if payload.emoji.name == '🎲' and len(self.gamblers) <= 1 and payload.member.name == self.game_creator:
                    await self.chan.send(f'{payload.member.name} -> We need more people to join before starting a game.')

            if payload.emoji.name == '🎲' and payload.member.name != self.game_creator:
                await self.chan.send(f"{payload.member.name} -> Sorry, only **{self.game_creator}** can start the game.", delete_after=10)
            if payload.emoji.name == '🗑️' and payload.member.name != self.game_creator:
                await self.chan.send(f"{payload.member.name} -> Sorry, only **{self.game_creator}** can cancel the game.", delete_after=10)
        else:
            return

    # Begin Rolling Function

    async def begin_roll(self):

        gamble_chan = self.bot.get_channel(int(self.GAMBLE_CHAN))

        if self.auto_roll == False:
            roll_embed = discord.Embed(title="Time to roll!", description=f"Type **.roll** now!", colour=discord.Color.red())
            roll_embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
            roll_embed.add_field(name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)

            await gamble_chan.send(embed=roll_embed)
        else:
            winner, loser, payout = self.bot_roll()

            roll_embed = discord.Embed(title="Rolls Completed!", description=f"Rolls were completed for the gambler.", colour=discord.Color.red())
            roll_embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
            roll_embed.add_field(name='Current Gamblers', value='None', inline=False)
            roll_embed.add_field(name="Results!", value=f"**{loser}** must pay **{payout}<:goldcoin:844724052294893568>** to **{winner}**!!")

            roll_list = []

            for k,v in self.gamblers_rolled.items():
                gambler = k
                roll = v
                roll_list.append(f'**{gambler}** rolled a **{roll}**')

            roll_embed.set_field_at(0, name='Current Gamblers and Rolls', value=f'\n'.join(g for g in roll_list), inline=False)
            await gamble_chan.send(embed=roll_embed)
            roll_list = []
        
            self.gamblers = []
            self.gamblers_rolled = {}
            self.gamble_amount = 0

    # Rolling Command

    @Command(name='roll', help='Type .roll to roll for the gambling session')
    async def roll(self, ctx: Context):

        if ctx.channel.id == int(self.GAMBLE_CHAN):
            print(self.gamblers)
            print(self.gamblers_rolled)

            if ctx.author.name in self.gamblers:
                if ctx.author.name in self.gamblers_rolled:
                    await ctx.send(f"{ctx.author.mention} -> Sorry, you've already rolled for this session.", delete_after=10)
                else:
                    random_num = Random(0, self.gamble_amount)
                    self.gamblers_rolled[ctx.author.mention] = random_num
                    await ctx.send(f'{ctx.author.mention} -> You rolled a {random_num}')

                    if len(self.gamblers_rolled) == len(self.gamblers):
                        highest_roll = int(self.gamblers_rolled[max(self.gamblers_rolled, key = self.gamblers_rolled.get)])
                        lowest_roll = int(self.gamblers_rolled[min(self.gamblers_rolled, key = self.gamblers_rolled.get)])
                        payout = highest_roll - lowest_roll

                        for k,v in self.gamblers_rolled.items():
                            if v == highest_roll:
                                winner = k
                            if v == lowest_roll:
                                loser = k
                        await ctx.send(f'{loser} must pay **{payout}<:goldcoin:844724052294893568>** to {winner}!')
                        self.gamblers = []
                        self.gamblers_rolled = {}
                        self.gamble_amount = 0

            else:
                await ctx.send(f"{ctx.author.mention} -> Sorry, you didn't enter before the game closed. Please join the next game.", delete_after=10)
        else:
            return

    # Automatic Bot Roll function

    def bot_roll(self):

        for gambler in self.gamblers:
            random_num = Random(0, self.gamble_amount)
            self.gamblers_rolled[gambler] = random_num

        highest_roll = int(self.gamblers_rolled[max(self.gamblers_rolled, key = self.gamblers_rolled.get)])
        lowest_roll = int(self.gamblers_rolled[min(self.gamblers_rolled, key = self.gamblers_rolled.get)])
        payout = highest_roll - lowest_roll

        for k,v in self.gamblers_rolled.items():
            if v == highest_roll:
                winner = k
            if v == lowest_roll:
                loser = k

        return winner, loser, payout

    # List of Gamblers Command

    @Command(name="gamblers", help="Lists all the current gamblers, and who hasn't rolled.")
    async def list_gamblers(self, ctx: Context):

        if ctx.channel.id == self.gamble_chan:
            if len(self.gamblers) == 0:
                await ctx.send(f"{ctx.author.mention} -> There is not an active game currently. To start a game, type **.gamble <amount>**", delete_after=10)
            else:

                missing_rolls = [i for i in self.gamblers if i not in self.gamblers_rolled]

                gambler_embed = discord.Embed(title="List of current gamblers", description="Here is a list of all gamblers.")
                gambler_embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
                gambler_embed.add_field(name="Gamblers in current session", value='\n'.join(g for g in self.gamblers), inline=False)
                gambler_embed.add_field(name="Gamblers who haven't rolled", value='\n'.join(g for g in missing_rolls), inline=False)
                await ctx.send(embed=gambler_embed)
        else:
            await ctx.send(f'{ctx.author.mention} -> Sorry, gambling is only available in the #gambling channel.', delete_after=10)

    # Current Gambling Session Command

    @Command(name='current', aliases=['cg'], help='Lists if there is a current game.')
    async def current_game(self, ctx: Context):

        if ctx.channel.id == int(self.GAMBLE_CHAN):
            if self.active_game == False:
                await ctx.send(f"{ctx.author.mention} -> Sorry, there isn't a current game. To start a game type .help gamble for help")
            else:
                await ctx.send(f"{ctx.author.mention} -> There is a current game, scroll up to join.")
        else:
            return

def setup(bot):
    bot.add_cog(Gamble(bot))