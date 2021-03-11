import discord
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context

class WowClass(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Death Knight Command

    @Command(
        name='dk',
        help='Displays class guide for Death Knight',
        usage='frost\n.dk blood\n.dk unholy')
    async def death_knight(self, ctx: Context, *, spec=None):
        
        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:blood:797202712214765598> Blood, <:frost:797201016860049488> Frost, or <:unholy:797202712193138709> Unholy?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'blood':
                await ctx.send(f'{ctx.author.mention} -> Here is the Blood Guide on WowHead\nhttps://www.wowhead.com/blood-death-knight-guide', delete_after=60)
            if msg.content.lower() == 'frost':
                await ctx.send(f'{ctx.author.mention} -> Here is the Frost Guide on WowHead\nhttps://www.wowhead.com/frost-death-knight-guide', delete_after=60)
            if msg.content.lower() == 'unholy' or msg.content.lower() == 'uh':
                await ctx.send(f'{ctx.author.mention} -> Here is the Unholy Guide on WowHead\nhttps://www.wowhead.com/unholy-death-knight-guide', delete_after=60)
        
        if spec.lower() == 'blood':
            await ctx.send(f'{ctx.author.mention} -> Here is the Blood Guide on WowHead\nhttps://www.wowhead.com/blood-death-knight-guide', delete_after=60)
        if spec.lower() == 'frost':
            await ctx.send(f'{ctx.author.mention} -> Here is the Frost Guide on WowHead\nhttps://www.wowhead.com/frost-death-knight-guide', delete_after=60)
        if spec.lower() == 'unholy' or spec.lower() == 'uh':
            await ctx.send(f'{ctx.author.mention} -> Here is the Unholy Guide on WowHead\nhttps://www.wowhead.com/unholy-death-knight-guide', delete_after=60)

    # Demon Hunter Command

    @Command(
        name='dh',
        help='Displays class guide for Demon Hunter',
        usage='havoc\n.dh vengeance')
    async def demon_hunter(self, ctx: Context, *, spec=None):
        
        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:havoc:797204927897665568> Havoc or <:vengeance:797204927939739658> Vengeance?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'havoc':
                await ctx.send(f'{ctx.author.mention} -> Here is the Havoc Guide on WowHead\nhttps://www.wowhead.com/havoc-demon-hunter-guide', delete_after=60)
            if msg.content.lower() == 'vengeance' or msg.content.lower() == 'veng':
                await ctx.send(f'{ctx.author.mention} -> Here is the Vengeance Guide on WowHead\nhttps://www.wowhead.com/vengeance-demon-hunter-guide', delete_after=60)
        
        if spec.lower() == 'havoc':
            await ctx.send(f'{ctx.author.mention} -> Here is the Havoc Guide on WowHead\nhttps://www.wowhead.com/havoc-demon-hunter-guide', delete_after=60)
        if spec.lower() == 'vengeance' or spec.lower() == 'veng':
            await ctx.send(f'{ctx.author.mention} -> Here is the Vengeance Guide on WowHead\nhttps://www.wowhead.com/vengeance-demon-hunter-guide', delete_after=60)
    
    # Druid Command

    @Command(
        name='druid',
        aliases=['dr'],
        help='Displays class guide for Druid',
        usage='feral\n.druid guardian\n.druid resto\n.dr boomkin')
    async def druid(self, ctx: Context, *, spec=None):
        
        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:feral:797202712156307507> Feral, <:guardian:797202712369561601> Guardian, <:restoration:797202712382537767> Resto, or <:balance:797202712156307566> Balance?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'feral' or msg.content.lower() == 'cat':
                await ctx.send(f'{ctx.author.mention} -> Here is the Feral Guide on WowHead\nhttps://www.wowhead.com/feral-druid-guide', delete_after=60)
            if msg.content.lower() == 'bear' or msg.content.lower() == 'burr' or msg.content.lower() == 'guardian':
                await ctx.send(f'{ctx.author.mention} -> Here is the Guardian Guide on WowHead\nhttps://www.wowhead.com/guardian-druid-guide', delete_after=60)
            if msg.content.lower() == 'resto':
                await ctx.send(f'{ctx.author.mention} -> Here is the Restoration Guide on WowHead\nhttps://www.wowhead.com/restoration-druid-guide', delete_after=60)
            if msg.content.lower() == 'balance' or msg.content.lower() == 'boomchicken' or msg.content.lower() == 'boomkin':
                await ctx.send(f'{ctx.author.mention} -> Here is the Balance Guide on WowHead\nhttps://www.wowhead.com/balance-druid-guide', delete_after=60)
        
        if spec.lower() == 'feral' or spec.lower() == 'cat':
            await ctx.send(f'{ctx.author.mention} -> Here is the Feral Guide on WowHead\nhttps://www.wowhead.com/feral-druid-guide', delete_after=60)
        if spec.lower() == 'bear' or spec.lower() == 'burr' or spec.lower() == 'guardian':
            await ctx.send(f'{ctx.author.mention} -> Here is the Guardian Guide on WowHead\nhttps://www.wowhead.com/guardian-druid-guide', delete_after=60)
        if spec.lower() == 'resto':
            await ctx.send(f'{ctx.author.mention} -> Here is the Restoration Guide on WowHead\nhttps://www.wowhead.com/restoration-druid-guide', delete_after=60)
        if spec.lower() == 'balance' or spec.lower() == 'boomchicken' or spec.lower() == 'boomkin':
            await ctx.send(f'{ctx.author.mention} -> Here is the Balance Guide on WowHead\nhttps://www.wowhead.com/balance-druid-guide', delete_after=60)

    # Hunter Command

    @Command(
        name='hunter',
        aliases=['hunt'],
        help='Displays class guide for Hunter',
        usage='mm\n.hunter bm\n.hunter surv')
    async def hunter(self, ctx: Context, *, spec=None):

        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:marksman:797202712306647070> Marksmanship, <:beastmastery:797202712143069194> Beast Mastery, or <:survival:797202712525537290> Survival?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'bm' or msg.content.lower() == 'beast' or msg.content.lower() == 'beast mastery':
                await ctx.send(f'{ctx.author.mention} -> Here is the Beast Mastery on WowHead\nhttps://www.wowhead.com/beast-mastery-hunter-guide', delete_after=60)
            if msg.content.lower() == 'mm' or msg.content.lower() == 'marks' or msg.content.lower() == 'marksman' or msg.content.lower() == 'marksmanship':
                await ctx.send(f'{ctx.author.mention} -> Here is the Marksmanship Guide on WowHead\nhttps://www.wowhead.com/marksmanship-hunter-guide', delete_after=60)
            if msg.content.lower() == 'survival' or msg.content.lower() == 'surv':
                await ctx.send(f'{ctx.author.mention} -> Here is the Survival Guide on WowHead\nhttps://www.wowhead.com/survival-hunter-guide', delete_after=60)
        
        if spec.lower() == 'bm' or spec.lower() == 'beast' or spec.lower() == 'beast mastery':
            await ctx.send(f'{ctx.author.mention} -> Here is the Beast Mastery Guide on WowHead\nhttps://www.wowhead.com/beast-mastery-hunter-guide', delete_after=60)
        if spec.lower() == 'mm' or spec.lower() == 'marks' or spec.lower() == 'marksman' or spec.lower() == 'marksmanship':
            await ctx.send(f'{ctx.author.mention} -> Here is the Marksmanship Guide on WowHead\nhttps://www.wowhead.com/marksmanship-hunter-guide', delete_after=60)
        if spec.lower() == 'survival' or spec.lower() == 'surv':
            await ctx.send(f'{ctx.author.mention} -> Here is the Survival Guide on WowHead\nhttps://www.wowhead.com/survival-hunter-guide', delete_after=60)

    # Mage Command

    @Command(
        name='mage',
        help='Displays class guide for Mage',
        usage='fire\n.mage frost\n .mage arcane')
    async def mage(self, ctx: Context, *, spec=None):
        
        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:mfire:797202712209915975> Fire, <:mfrost:797202712448991262> Frost, or <:arcane:790339486600921158> Arcane?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'fire':
                await ctx.send(f'{ctx.author.mention} -> Here is the Fire Guide on WowHead\nhttps://www.wowhead.com/fire-mage-guide', delete_after=60)
            if msg.content.lower() == 'frost':
                await ctx.send(f'{ctx.author.mention} -> Here is the Frost Guide on WowHead\nhttps://www.wowhead.com/frost-mage-guide', delete_after=60)
            if msg.content.lower() == 'arcane':
                await ctx.send(f'{ctx.author.mention} -> Here is the Arcane Guide on WowHead\nhttps://www.wowhead.com/arcane-mage-guide', delete_after=60)
        
        if spec.lower() == 'fire':
            await ctx.send(f'{ctx.author.mention} -> Here is the Fire Guide on WowHead\nhttps://www.wowhead.com/fire-mage-guide', delete_after=60)
        if spec.lower() == 'frost':
            await ctx.send(f'{ctx.author.mention} -> Here is the Frost Guide on WowHead\nhttps://www.wowhead.com/frost-mage-guide', delete_after=60)
        if spec.lower() == 'arcane':
            await ctx.send(f'{ctx.author.mention} -> Here is the Arcane Guide on WowHead\nhttps://www.wowhead.com/arcane-mage-guide', delete_after=60)

    # Monk Command

    @Command(
        name='monk',
        help='Displays class guide for Monk',
        usage='bm\n.monk windwalker\n.monk mist')
    async def monk(self, ctx: Context, *, spec=None):
        
        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:brewmaster:797202712143724574> Brewmaster, <:windwalker:797202712180686869> Windwalker, or <:mistweaver:797202712382275654> Mistweaver?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'brewmaster' or msg.content.lower() == 'bm':
                await ctx.send(f'{ctx.author.mention} -> Here is the Brewmaster Guide on WowHead\nhttps://www.wowhead.com/brewmaster-monk-guide', delete_after=60)
            if msg.content.lower() == 'windwalker' or msg.content.lower() == 'ww':
                await ctx.send(f'{ctx.author.mention} -> Here is the Windwalker Guide on WowHead\nhttps://www.wowhead.com/windwalker-monk-guide', delete_after=60)
            if msg.content.lower() == 'mistweaver' or msg.content.lower() == 'mw' or msg.content.lower() == 'mist':
                await ctx.send(f'{ctx.author.mention} -> Here is the Mistweaver Guide on WowHead\nhttps://www.wowhead.com/mistweaver-monk-guide', delete_after=60)
        
        if spec.lower() == 'brewmaster' or spec.lower() == 'bm':
            await ctx.send(f'{ctx.author.mention} -> Here is the Brewmaster Guide on WowHead\nhttps://www.wowhead.com/brewmaster-monk-guide', delete_after=60)
        if spec.lower() == 'windwalker' or spec.lower() =='ww':
            await ctx.send(f'{ctx.author.mention} -> Here is the Windwalker Guide on WowHead\nhttps://www.wowhead.com/windwalker-monk-guide', delete_after=60)
        if spec.lower() == 'mistweaver' or spec.lower() == 'mw' or spec.lower() == 'mist':
            await ctx.send(f'{ctx.author.mention} -> Here is the Mistweaver Guide on WowHead\nhttps://www.wowhead.com/mistweaver-monk-guide', delete_after=60)

    # Paladin Command

    @Command(
        name='paladin',
        aliases=['paly'],
        help='Displays class guide for Paladin',
        usage='prot\n.paly retribution\n.paly holy')
    async def paladin(self, ctx: Context, *, spec=None):
        
        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:protection:797202712282398731> Protection, <:retribution:797202712357896253> Retribution, or <:pholy:797202712092606525> Holy?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'retribution' or msg.content.lower() == 'ret':
                await ctx.send(f'{ctx.author.mention} -> Here is the Retribution Guide on WowHead\nhttps://www.wowhead.com/retribution-paladin-guide', delete_after=60)
            if msg.content.lower() == 'protection' or msg.content.lower() == 'prot':
                await ctx.send(f'{ctx.author.mention} -> Here is the Protection Guide on WowHead\nhttps://www.wowhead.com/protection-paladin-guide', delete_after=60)
            if msg.content.lower() == 'holy':
                await ctx.send(f'{ctx.author.mention} -> Here is the Holy Guide on WowHead\nhttps://www.wowhead.com/holy-paladin-guide', delete_after=60)
        
        if spec.lower() == 'retribution' or spec.lower() == 'ret':
            await ctx.send(f'{ctx.author.mention} -> Here is the Retribution Guide on WowHead\nhttps://www.wowhead.com/retribution-paladin-guide', delete_after=60)
        if spec.lower() == 'protection' or spec.lower() =='prot':
            await ctx.send(f'{ctx.author.mention} -> Here is the Protection Guide on WowHead\nhttps://www.wowhead.com/protection-paladin-guide', delete_after=60)
        if spec.lower() == 'holy':
            await ctx.send(f'{ctx.author.mention} -> Here is the Holy Guide on WowHead\nhttps://www.wowhead.com/holy-paladin-guide', delete_after=60)

    # Priest Command

    @Command(
        name='priest',
        help='Displays class guide for Priest',
        usage='shadow\n.priest disc\n.priest holy')
    async def priest(self, ctx: Context, *, spec=None):
        
        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:discipline:797202712004526172> Discipline, <:shadow:797202712374280243> Shadow, or <:holy:797202712479006810> Holy?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'discipline' or msg.content.lower() == 'disc':
                await ctx.send(f'{ctx.author.mention} -> Here is the Discipline Guide on WowHead\nhttps://www.wowhead.com/discipline-priest-guide', delete_after=60)
            if msg.content.lower() == 'shadow':
                await ctx.send(f'{ctx.author.mention} -> Here is the Shadow Guide on WowHead\nhttps://www.wowhead.com/shadow-priest-guide', delete_after=60)
            if msg.content.lower() == 'holy':
                await ctx.send(f'{ctx.author.mention} -> Here is the Holy Guide on WowHead\nhttps://www.wowhead.com/holy-priest-guide', delete_after=60)
        
        if spec.lower() == 'disipline' or spec.lower() == 'disc':
            await ctx.send(f'{ctx.author.mention} -> Here is the Discipline Guide on WowHead\nhttps://www.wowhead.com/discipline-priest-guide', delete_after=60)
        if spec.lower() == 'shadow':
            await ctx.send(f'{ctx.author.mention} -> Here is the Shadow Guide on WowHead\nhttps://www.wowhead.com/shadow-priest-guide', delete_after=60)
        if spec.lower() == 'holy':
            await ctx.send(f'{ctx.author.mention} -> Here is the Holy Guide on WowHead\nhttps://www.wowhead.com/holy-priest-guide', delete_after=60)

    # Priest Command

    @Command(
        name='rogue',
        help='Displays class guide for Rogue',
        usage='sub\n.rogue ass\n.rogue outlaw')
    async def rogue(self, ctx: Context, *, spec=None):
        
        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:assassination:797202712290787399> Assassination, <:subtlety:797206736041803796> Subtlety, or <:outlaw:797202712310841354> Outlaw?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'assassination' or msg.content.lower() == 'ass':
                await ctx.send(f'{ctx.author.mention} -> Here is the Assassination Guide on WowHead\nhttps://www.wowhead.com/assassination-rogue-guide', delete_after=60)
            if msg.content.lower() == 'subtlely' or msg.content.lower() == 'sub':
                await ctx.send(f'{ctx.author.mention} -> Here is the Subtlety Guide on WowHead\nhttps://www.wowhead.com/subtlety-rogue-guide', delete_after=60)
            if msg.content.lower() == 'outlaw':
                await ctx.send(f'{ctx.author.mention} -> Here is the Outlaw Guide on WowHead\nhttps://www.wowhead.com/outlaw-rogue-guide', delete_after=60)
        
        if spec.lower() == 'assassination' or spec.lower() == 'ass':
            await ctx.send(f'{ctx.author.mention} -> Here is the Assassination Guide on WowHead\nhttps://www.wowhead.com/assassination-rogue-guide', delete_after=60)
        if spec.lower() == 'subtlely' or spec.lower() == 'sub':
            await ctx.send(f'{ctx.author.mention} -> Here is the Subtlely Guide on WowHead\nhttps://www.wowhead.com/subtlety-rogue-guide', delete_after=60)
        if spec.lower() == 'outlaw':
            await ctx.send(f'{ctx.author.mention} -> Here is the Outlaw Guide on WowHead\nhttps://www.wowhead.com/outlaw-rogue-guide', delete_after=60)

    # Shaman Command

    @Command(
        name='shaman',
        aliases=['sham'],
        help='Displays class guide for Shaman',
        usage='resto\n.shaman enh\n.sham elemental')
    async def shaman(self, ctx: Context, *, spec=None):

        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:enhancement:797202712160501770> Enhancement, <:elemental:797202712247795772> Elemental, or <:srestoration:797202712382668800> Resto?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'enhancement' or msg.content.lower() == 'enh':
                await ctx.send(f'{ctx.author.mention} -> Here is the Enhancement Guide on WowHead\nhttps://www.wowhead.com/enhancement-shaman-guide', delete_after=60)
            if msg.content.lower() == 'elemental' or msg.content.lower() == 'ele':
                await ctx.send(f'{ctx.author.mention} -> Here is the Elemental Guide on WowHead\nhttps://www.wowhead.com/elemental-shaman-guide', delete_after=60)
            if msg.content.lower() == 'resto':
                await ctx.send(f'{ctx.author.mention} -> Here is the Restoration Guide on WowHead\nhttps://www.wowhead.com/restoration-shaman-guide', delete_after=60)
        
        if spec.lower() == 'enhancement' or spec.lower() == 'enh':
            await ctx.send(f'{ctx.author.mention} -> Here is the Enhancement Guide on WowHead\nhttps://www.wowhead.com/enhancement-shaman-guide', delete_after=60)
        if spec.lower() == 'elemental' or spec.lower() == 'ele':
            await ctx.send(f'{ctx.author.mention} -> Here is the Elemental Guide on WowHead\nhttps://www.wowhead.com/elemental-shaman-guide', delete_after=60)
        if spec.lower() == 'resto':
            await ctx.send(f'{ctx.author.mention} -> Here is the Restoration Guide on WowHead\nhttps://www.wowhead.com/restoration-shaman-guide', delete_after=60)

    # Warlock Command

    @Command(
        name='warlock',
        aliases=['lock'],
        help='Displays class guide for Warlock',
        usage='aff\n.lock destro\n.warlock demonology')
    async def warlock(self, ctx: Context, *, spec=None):

        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:affliction:797202711870701579> Affliction, <:demonology:797202712194318387> Demonology, or <:destruction:797202712114233375> Destruction?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'affliction' or msg.content.lower() == 'aff':
                await ctx.send(f'{ctx.author.mention} -> Here is the Affliction Guide on WowHead\nhttps://www.wowhead.com/affliction-warlock-guide', delete_after=60)
            if msg.content.lower() == 'demonology' or msg.content.lower() == 'demo':
                await ctx.send(f'{ctx.author.mention} -> Here is the Demonology Guide on WowHead\nhttps://www.wowhead.com/demonology-warlock-guide', delete_after=60)
            if msg.content.lower() == 'destruction' or msg.content.lower() == 'destro':
                await ctx.send(f'{ctx.author.mention} -> Here is the Destruction Guide on WowHead\nhttps://www.wowhead.com/destruction-warlock-guide', delete_after=60)
        
        if spec.lower() == 'afflication' or spec.lower() == 'aff':
            await ctx.send(f'{ctx.author.mention} -> Here is the Affliction Guide on WowHead\nhttps://www.wowhead.com/affliction-warlock-guide', delete_after=60)
        if spec.lower() == 'demonology' or spec.lower() == 'demo':
            await ctx.send(f'{ctx.author.mention} -> Here is the Demonology Guide on WowHead\nhttps://www.wowhead.com/demonology-warlock-guide', delete_after=60)
        if spec.lower() == 'destruction' or spec.lower() == 'destro':
            await ctx.send(f'{ctx.author.mention} -> Here is the Destruction Guide on WowHead\nhttps://www.wowhead.com/destruction-warlock-guide', delete_after=60)
    
    # Warrior Command

    @Command(
        name='warrior',
        aliases=['warr'],
        help='Displays class guide for Warrior',
        usage='prot\n.warrior arms\n.warr fury')
    async def warrior(self, ctx: Context, *, spec=None):

        if spec == None:
            await ctx.send(f'{ctx.author.mention} -> Which spec? <:arms:797202712201527316> Arms, <:fury:797202712264704000>  Fury, or <:wprotection:797202712718082068> Protection?', delete_after=60)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

            if msg.content.lower() == 'arms':
                await ctx.send(f'{ctx.author.mention} -> Here is the Arms Guide on WowHead\nhttps://www.wowhead.com/arms-warrior-guide', delete_after=60)
            if msg.content.lower() == 'fury':
                await ctx.send(f'{ctx.author.mention} -> Here is the Fury Guide on WowHead\nhttps://www.wowhead.com/fury-warrior-guide', delete_after=60)
            if msg.content.lower() == 'protection' or msg.content.lower() == 'prot':
                await ctx.send(f'{ctx.author.mention} -> Here is the Protection Guide on WowHead\nhttps://www.wowhead.com/protection-warrior-guide', delete_after=60)
        
        if spec.lower() == 'arms':
            await ctx.send(f'{ctx.author.mention} -> Here is the Arms Guide on WowHead\nhttps://www.wowhead.com/arms-warrior-guide', delete_after=60)
        if spec.lower() == 'fury':
            await ctx.send(f'{ctx.author.mention} -> Here is the Fury Guide on WowHead\nhttps://www.wowhead.com/fury-warrior-guide', delete_after=60)
        if spec.lower() == 'protection' or spec.lower() == 'prot':
            await ctx.send(f'{ctx.author.mention} -> Here is the Protection Guide on WowHead\nhttps://www.wowhead.com/protection-warrior-guide', delete_after=60)

    # WarcraftLogs How-to Command

    @Command(
        name='warcraftlogs',
        aliases=['wl'],
        help='This will link a YouTube Video for how to examine WarcraftLogs to increase your performance.')
    async def warcraft_logs(self, ctx: Context):
        await ctx.send(f'{ctx.author.mention} -> This link will show you how to utilize WarcraftLogs to increase your dps/hps during raids.\nhttps://www.youtube.com/watch?v=sbY_t53Zj1A')

    # DPS Ranks Command

    @Command(
        name='ranks',
        help='Displays the current DPS Ranks in raid')
    async def ranks(self, ctx: Context):
        await ctx.send(f"{ctx.author.mention} -> Here are the current DPS ranks.\nhttps://i.imgur.com/vFhfq0V.png")
    

def setup(bot):
    bot.add_cog(WowClass(bot))
