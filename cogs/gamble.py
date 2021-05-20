import discord
from random import randint as Random
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context


class Gamble(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.active_game = False
        self.gamble_amount = 0
        self.gamblers = []
        self.gamblers_rolled = {}
        self.curr_chan = 0
        
    @Command(name='gamble', aliases=['g'], help='To start a game, type .gamble <amount>')
    async def start_game(self, ctx: Context, amount: int):

        if self.active_game == False:
            self.active_game = True
            self.gamble_amount = amount
            self.current_channel = ctx.channel.id
            self.game_creator = ctx.author.name

            embed = discord.Embed(title="World of Warcraft Gold Gambling has started!", description=f'HiLo roll for **{self.gamble_amount}<:goldcoin:844724052294893568>**. Started by **{ctx.author.mention}**', colour=discord.Colour.orange())
            embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
            embed.add_field(name='🟢 Entry', value='To **join**, click ✅\nTo **leave**, click ❌', inline=False)
            embed.add_field(name='📄 Rules', value='1. You must pay in game at your earliest convenience\n2. Xylr will be notified of winner and amount\n3. Have fun and be respectful!', inline=False)
            embed.add_field(name='🛠️ Instructions', value='**Only the game starter can use the commands below**\nClick 🎲 to start the game\nClick 🗑️ to cancel the game', inline=False)
            embed.add_field(name='Current Gamblers', value='None', inline=False)
            
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❌')
            await msg.add_reaction('🎲')
            await msg.add_reaction('🗑️')

        else:
            await ctx.send(f'{ctx.author.mention} -> There is already an active game. Use command .current for more information')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.bot:
            return
        self.chan = self.bot.get_channel(payload.channel_id)
        msg = await self.chan.fetch_message(payload.message_id)
        embed = msg.embeds[0]

        if payload.emoji.name == '🗑️' and payload.member.name == self.game_creator:
            self.active_game = False
            cancel_embed = discord.Embed(title="World of Warcraft Gold Gambling has been cancelled!", description=f'Cancelled by **{self.game_creator}**', colour=discord.Colour.orange())
            cancel_embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
            cancel_embed.add_field(name='❌ Cancelled', value='Gamble entry has been cancelled.', inline=False)
            await msg.edit(embed=cancel_embed)
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
                if not payload.member.mention in embed_dict['fields'][3]['value']:
                    if 'None' in self.gamblers:
                        self.gamblers.remove('None')
                        self.gamblers.append(payload.member.mention)
                        embed.set_field_at(3, name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)
                    else:
                        self.gamblers.append(payload.member.mention)
                        embed.set_field_at(3, name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)

            if payload.emoji.name == '❌':
                embed_dict = embed.to_dict()
                if payload.member.mention in embed_dict['fields'][3]['value']:
                    self.gamblers.remove(payload.member.mention)
                    if len(self.gamblers) == 0:
                        self.gamblers.append('None')
                        embed.set_field_at(3, name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)
                    else:
                        embed.set_field_at(3, name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)


            await msg.edit(embed=embed)
            await msg.remove_reaction(payload.emoji, payload.member)

            if payload.emoji.name == '🎲' and len(self.gamblers) <= 1 and payload.member.name == self.game_creator:
                await self.chan.send(f'{payload.member.mention} -> We need more people to join before starting a game.')

        if payload.emoji.name == '🎲' and payload.member.name != self.game_creator:
            await self.chan.send(f"{payload.member.mention} -> Sorry, only the game starter can start the game.")
        if payload.emoji.name == '🗑️' and payload.member.name != self.game_creator:
            await self.chan.send(f"{payload.member.mention} -> Sorry, only the game starter can cancel the game.")

    async def begin_roll(self):

        test_embed = discord.Embed(title="Time to roll!", description=f"Type **.roll** now!")
        test_embed.add_field(name='Current Gamblers', value='\n'.join(g for g in self.gamblers), inline=False)

        await self.chan.send(embed=test_embed)

    @Command(name='roll', help='Type .roll to roll for the gambling session')
    async def roll(self, ctx: Context):

        if ctx.author.mention not in self.gamblers:
            await ctx.send(f'{ctx.author.mention} -> There is no active game currently. To start a game, type ".gamble <amount>".')

        else:

            if ctx.author.mention in self.gamblers:
                if ctx.author.mention in self.gamblers_rolled:
                    await ctx.send(f"{ctx.author.mention} -> Sorry, you've already rolled for this session.")
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
                await ctx.send(f"{ctx.author.mention} -> Sorry, you didn't enter before the game ended. Please join the next game.")

    @Command(name="gamblers", help="Lists all the current gamblers, and who hasn't rolled.")
    async def list_gamblers(self, ctx: Context):

        if len(self.gamblers) == 0:
            await ctx.send(f"{ctx.author.mention} -> There is not an active game currently. To start a game, type **.gamble <amount>**")
        else:

            missing_rolls = [i for i in self.gamblers if i not in self.gamblers_rolled]

            gambler_embed = discord.Embed(title="List of current gamblers", description="Here is a list of all gamblers.")
            gambler_embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
            gambler_embed.add_field(name="Gamblers in current session", value='\n'.join(g for g in self.gamblers), inline=False)
            gambler_embed.add_field(name="Gamblers who haven't rolled", value='\n'.join(g for g in missing_rolls), inline=False)
            await ctx.send(embed=gambler_embed)

def setup(bot):
    bot.add_cog(Gamble(bot))