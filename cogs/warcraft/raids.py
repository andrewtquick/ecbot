from discord.ext import commands
from discord.ext.commands import Context
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class Raids(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Raid Guide Command

    @cog_ext.cog_slash(
        name='raid-guide',
        description='Display information regarding the boss and difficulty you select',
        options=[
            create_option(
                name='difficulty',
                description='Select a difficulty',
                required=True,
                option_type=3,
                choices=[
                    create_choice(name='Normal', value='normal'),
                    create_choice(name='Heroic', value='hero'),
                    create_choice(name='Mythic', value='myth')]
            ),
            create_option(
                name='boss',
                description='Select the raid boss',
                required=True,
                option_type=3,
                choices=[
                    create_choice(name='The Tarragrue', value='tarra'),
                    create_choice(name='The Eye of the Jailer', value='eye'),
                    create_choice(name='The Nine', value='nine'),
                    create_choice(name='Soulrender Doirmazain', value='soul'),
                    create_choice(name="Remnant of Ner'zhul", value='remnant'),
                    create_choice(name='Painsmith Raznal', value='raznal'),
                    create_choice(name='Guardian of the First Ones', value='guard'),
                    create_choice(name='Fatescribe Roh-Kalo', value='kalo'),
                    create_choice(name="Kel'Thuzad", value='kel'),
                    create_choice(name='Sylvanas Windrunner', value='sylvanas'),
                    create_choice(name='Shriekwing', value='shriek'),
                    create_choice(name='Huntsman Altimor', value='hunts'),
                    create_choice(name='Hungering Destroyer', value='hung'),
                    create_choice(name="Artificer Xy'Mox", value='xymox'),
                    create_choice(name="Sun King's Salvation", value='king'),
                    create_choice(name='Lady Inerva Darkvein', value='lady'),
                    create_choice(name='Council of Blood', value='council'),
                    create_choice(name='Sludgefist', value='sludge'),
                    create_choice(name='Stone Legion', value='stone'),
                    create_choice(name='Sire Denathrius', value='sire')]
            )])
    async def castle_nathria(self, ctx: Context, boss, difficulty):

        raid_guides = {
            'shriek': {
                'name': 'Shriekwing',
                'normal': 'https://mythictrap.com/castleNathria/shriekwing/normal/',
                'hero': 'https://mythictrap.com/castleNathria/shriekwing/heroic/',
                'myth': 'https://mythictrap.com/castleNathria/shriekwing/mythic'
            },
            'hunts': {
                'name': 'Huntsman Altimor',
                'normal': 'https://mythictrap.com/castleNathria/altimor/normal/',
                'hero': 'https://mythictrap.com/castleNathria/altimor/heroic/',
                'myth': 'https://mythictrap.com/castleNathria/altimor/mythic/'
            },
            'hung': {
                'name': 'Hungering Destroyer',
                'normal': 'https://mythictrap.com/castleNathria/hungeringDestroyer/normal/',
                'hero': 'https://mythictrap.com/castleNathria/hungeringDestroyer/heroic/',
                'myth': 'https://mythictrap.com/castleNathria/hungeringDestroyer/mythic/'
            },
            'xymox': {
                'name': "Artificer Xy'Mox",
                'normal': 'https://mythictrap.com/castleNathria/artificerXyMox/normal/',
                'hero': 'https://mythictrap.com/castleNathria/artificerXyMox/heroic/',
                'myth': 'https://mythictrap.com/castleNathria/artificerXyMox/mythic/'
            },
            'king': {
                'name': "Sun King's Salvation",
                'normal': 'https://mythictrap.com/castleNathria/sunkingssalvation/normal/',
                'hero': 'https://mythictrap.com/castleNathria/sunkingssalvation/heroic/',
                'myth': 'https://mythictrap.com/castleNathria/sunkingssalvation/mythic/'
            },
            'lady': {
                'name': 'Lady Inerva Darkvein',
                'normal': 'https://mythictrap.com/castleNathria/ladyInervaDarkvein/normal/',
                'hero': 'https://mythictrap.com/castleNathria/ladyInervaDarkvein/heroic/',
                'myth': 'https://mythictrap.com/castleNathria/ladyInervaDarkvein/mythic/'
            },
            'council': {
                'name': 'Council of Blood',
                'normal': 'https://mythictrap.com/castleNathria/theCouncilOfBlood/normal/',
                'hero': 'https://mythictrap.com/castleNathria/theCouncilOfBlood/heroic/',
                'myth': 'https://mythictrap.com/castleNathria/theCouncilOfBlood/mythic/'
            },
            'sludge': {
                'name': 'Sludgefist',
                'normal': 'https://mythictrap.com/castleNathria/sludgefist/normal/',
                'hero': 'https://mythictrap.com/castleNathria/sludgefist/heroic/',
                'myth': 'https://mythictrap.com/castleNathria/sludgefist/mythic/'
            },
            'stone': {
                'name': 'Stone Legion',
                'normal': 'https://mythictrap.com/castleNathria/stoneLegionGenerals/normal/',
                'hero': 'https://mythictrap.com/castleNathria/stoneLegionGenerals/herioc/',
                'myth': 'https://mythictrap.com/castleNathria/stoneLegionGenerals/mythic/'
            },
            'sire': {
                'name': 'Sire Denathrius',
                'normal': 'https://mythictrap.com/castleNathria/sireDenathrius/normal/',
                'hero': 'https://mythictrap.com/castleNathria/sireDenathrius/heroic/',
                'myth': 'https://mythictrap.com/castleNathria/sireDenathrius/mythic/'
            },
            'tarra': {
                'name': 'The Tarragrue',
                'normal': 'https://mythictrap.com/sanctumOfDomination/tarragrue/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/tarragrue/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/tarragrue/mythic/none'
            },
            'eye': {
                'name': 'The Eye of the Jailer',
                'normal': 'https://mythictrap.com/sanctumOfDomination/eyeOfTheJailer/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/eyeOfTheJailer/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/eyeOfTheJailer/mythic/none'
            },
            'nine': {
                'name': 'The Nine',
                'normal': 'https://mythictrap.com/sanctumOfDomination/theNine/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/theNine/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/theNine/mythic/none'
            },
            'remnant': {
                'name': "Remnant of Ner'Zhul",
                'normal': 'https://mythictrap.com/sanctumOfDomination/nerZhul/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/nerZhul/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/nerZhul/mythic/none'
            },
            'soul': {
                'name': 'Soulrender Dormazain',
                'normal': 'https://mythictrap.com/sanctumOfDomination/dormazain/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/dormazain/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/dormazain/mythic/none'
            },
            'raznal': {
                'name': 'Painsmith Raznal',
                'normal': 'https://mythictrap.com/sanctumOfDomination/raznal/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/raznal/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/raznal/mythic/none'
            },
            'guard': {
                'name': 'Guardian of the First Ones',
                'normal': 'https://mythictrap.com/sanctumOfDomination/guardian/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/guardian/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/guardian/mythic/none'
            },
            'kalo': {
                'name': 'Fatescribe Roh-Kalo',
                'normal': 'https://mythictrap.com/sanctumOfDomination/rohKalo/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/rohKalo/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/rohKalo/mythic/none'
            },
            'kel': {
                'name': "Kel'Thuzad",
                'normal': 'https://mythictrap.com/sanctumOfDomination/kelThuzad/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/kelThuzad/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/kelThuzad/mythic/none'
            },
            'sylvanas': {
                'name': 'Sylvanas Windrunner',
                'normal': 'https://mythictrap.com/sanctumOfDomination/sylvanas/normal/none',
                'hero': 'https://mythictrap.com/sanctumOfDomination/sylvanas/heroic/none',
                'myth': 'https://mythictrap.com/sanctumOfDomination/sylvanas/mythic/none'
            }}
        
        if difficulty == 'normal':
            await ctx.send(content=f"{ctx.author.mention} -> Here is the `Normal` guide for `{raid_guides[boss]['name']}`\n\n{raid_guides[boss]['normal']}")
        if difficulty == 'hero':
            await ctx.send(content=f"{ctx.author.mention} -> Here is the `Heroic` guide for `{raid_guides[boss]['name']}`\n\n{raid_guides[boss]['hero']}")
        if difficulty == 'myth':
            await ctx.send(content=f"{ctx.author.mention} -> Here is the `Mythic` guide for `{raid_guides[boss]['name']}`\n\n{raid_guides[boss]['myth']}")

def setup(bot):
    bot.add_cog(Raids(bot))