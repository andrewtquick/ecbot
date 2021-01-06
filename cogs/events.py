import discord
import os
from discord.ext import commands
from discord.ext.commands import command as Command
from discord.ext.commands import Context

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.OFFICER_CHANNEL = os.getenv('OFFICER_CHANNEL')
        self.PURGATORY_CHAN = os.getenv('PURGATORY_CHAN')
        self.EC_GUILD = os.getenv('GUILD')

    # On Ready

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} online.')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='.help command'))

    # On Member Remove or Leave

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        ochannel = self.bot.get_channel(int(self.OFFICER_CHANNEL))
        ec_guild = self.bot.get_guild(int(self.EC_GUILD))

        async for entry in ec_guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if isinstance(entry.action, type(discord.AuditLogAction.kick)):
                print(discord.AuditLogEntry.created_at)
        #         await ochannel.send(f"**{entry.user.name}** kicked **{entry.target.name}** from the server.")
        #         return

        # async for entry in ec_guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        #     if isinstance(entry.action, type(discord.AuditLogAction.ban)):
        #         await ochannel.send(f"**{entry.user.name}** banned **{entry.target.name}** from the server.")
        #         return

        # await ochannel.send(f'**{member}** has left the server.')

    # On Member Join Message

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        ochannel = self.bot.get_channel(int(self.PURGATORY_CHAN))

        await ochannel.send(f'**{member.name}** has joined the server.')

        embed = discord.Embed(
            title="Welcome to Elite Casual's Discord Server",
            description='We are an AOTC focused raiding guild on Stormrage-US\n\u200b',
            colour=discord.Colour.blue())
        embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
        embed.add_field(name='📄 Server Rules 📄', value='❌ No Racism\n❌ No Politics Discussion\n❌ No Toxicity\n❌ No NSFW Content\n✅ Have fun!\n\n**These rules are zero tolerance.**\n\u200b', inline=False)
        embed.add_field(name='👑 Guild Leadership 👑', value='Xylr\nDiamondclaw\nZellah\n\u200b', inline=False)
        embed.add_field(name='❔ Looking to raid or just hang out? ❔', value='Please be sure to reach out to the guild leadership with your intention.', inline=False)
        await member.send('https://i.imgur.com/gYeYMCM.png')
        await member.send(embed=embed)

    # Member Role Update Notifier

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        ochannel = self.bot.get_channel(int(self.OFFICER_CHANNEL))
        ec_guild = self.bot.get_guild(int(self.EC_GUILD))
        new_role = [role for role in after.roles if role not in before.roles]
        old_role = [role for role in before.roles if role not in after.roles]

        if old_role:
            async for entry in ec_guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                if entry.user.name == "ECDev" or entry.user.name == "Elite Casual Mod":
                    pass
                else:
                    await ochannel.send(f"**{entry.user.name}** removed the `{old_role[0].name}` role from **{entry.target.name}**.")
        
        if new_role:
            async for entry in ec_guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                if entry.user.name == "ECDev" or entry.user.name == "Elite Casual Mod":
                    pass
                else:
                    await ochannel.send(f"**{entry.user.name}** added the `{new_role[0].name}` role to **{entry.target.name}**.")


def setup(bot):
    bot.add_cog(Events(bot))