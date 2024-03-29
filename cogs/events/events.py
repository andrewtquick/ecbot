import discord
import os
from misc.firebase import DBConnection
from misc.utils import Utils
from datetime import datetime as dt
from datetime import timedelta
from discord import Member as Member
from discord.ext import commands
from firebase_admin import db

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.O_CHAN_GET = os.getenv('OFFICER_CHANNEL')
        self.PURG_CHAN_GET = os.getenv('PURGATORY_CHAN')
        self.EC_GUILD_GET = os.getenv('GUILD')
        self.ecdb = DBConnection()
        self.utils = Utils(self)

    # On Ready

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} online.')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='.help command'))
        self.gather_all_members()

    # On Member Leave, Kick, and Ban

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        self.O_CHANNEL = self.bot.get_channel(int(self.O_CHAN_GET))
        self.EC_GUILD = self.bot.get_guild(int(self.EC_GUILD_GET))

        await self.O_CHANNEL.send(f"**{member.display_name} ({member})** has left the server.")
        user_ref = db.reference()
        member_left = user_ref.child(str(member.guild.id)).child('users').child(str(member.id))
        member_left.update({'left': self.utils.parse_date_time(dt.now())})

     # On Member Unban

    @commands.Cog.listener()
    async def on_member_unban(self, _, __):
        self.O_CHANNEL = self.bot.get_channel(int(self.O_CHAN_GET))
        self.EC_GUILD = self.bot.get_guild(int(self.EC_GUILD_GET))

        async for entry in self.EC_GUILD.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            await self.O_CHANNEL.send(f"**{entry.user.name}** unbanned **{entry.target}** from the server.")

    # On Member Join Message

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        self.O_CHANNEL = self.bot.get_channel(int(self.O_CHAN_GET))
        await self.O_CHANNEL.send(f"**{member.name}** has joined the server.")
        get_embed = self.rules_embed()
        self.ecdb.add_new_user(member.guild, member)
        await member.send('https://i.imgur.com/gYeYMCM.png')
        await member.send(embed=get_embed)

    # Member Role Update and Nickname Change Notifier

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        self.O_CHANNEL = self.bot.get_channel(int(self.O_CHAN_GET))
        self.EC_GUILD = self.bot.get_guild(int(self.EC_GUILD_GET))

        new_role = [role for role in after.roles if role not in before.roles]
        old_role = [role for role in before.roles if role not in after.roles]

        if old_role:
            async for entry in self.EC_GUILD.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                if entry.user.name != self.bot.user.name:
                    await self.O_CHANNEL.send(f"**{entry.user.name}** removed the `{old_role[0].name}` role from **{entry.target.display_name}**.")
        
        if new_role:
            async for entry in self.EC_GUILD.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                if new_role[0].name == 'Server Booster':
                    await self.O_CHANNEL.send(f"**{entry.user.name}** just boosted the server!")

                if entry.user.name != self.bot.user.name:
                    await self.O_CHANNEL.send(f"**{entry.user.name}** added the `{new_role[0].name}` role to **{entry.target.display_name}**.")

        if before.nick != after.nick:
            user_ref = db.reference(str(before.guild.id)).child('users')
            name_change = user_ref.child(str(before.id))
            check_nick = name_change.get()

            async for entry in self.EC_GUILD.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
                if before.name != entry.user.name:
                    if entry.user.name != self.bot.user.name:
                        await self.O_CHANNEL.send(f"**{entry.user.name}** changed `{before.name}`'s nickname to **{entry.target.display_name}**.")
                else:
                    await self.O_CHANNEL.send(f"**{before}** changed their nickname to **{entry.target.display_name}**")
                
                if 'nickname' in check_nick:
                    names_set = []
                    for k,v in check_nick.items():
                        if k == 'nickname':
                            names_set.append(v)
                    names_set.append(entry.target.display_name)
                    name_change.update({ 'nickname': ', '.join(name for name in names_set) })
                else:
                    name_change.update({ 'nickname': entry.target.display_name })

    # Rules Embed Function

    def rules_embed(self):
        embed = discord.Embed(
            title="Welcome to Elite Casual's Discord Server",
            description='We are an AOTC focused raiding guild on Stormrage-US\n\u200b',
            colour=discord.Colour.blue())
        embed.set_thumbnail(url='https://i.imgur.com/eWMZmVV.png')
        embed.add_field(name='📄 Server Rules 📄', value='❌ No Racism\n❌ No Politics Discussion\n❌ No Toxicity\n❌ No NSFW Content\n✅ Have fun!\n\n**These rules are zero tolerance.**\n\u200b', inline=False)
        embed.add_field(name='👑 Guild Leadership 👑', value='Xylr\nDiamondclaw\nZellah\n\u200b', inline=False)
        embed.add_field(name='🔱 Guild Advisor 🔱', value='Jaemyst\nFuzzybottomz\n\u200b', inline=False)
        embed.add_field(name='❔ Looking to raid? ❔', value='Please be sure to reach out to the guild leadership with your intention.', inline=False)
        return embed

    # Gathering all user information on ready

    def gather_all_members(self):
        guilds = self.bot.guilds

        for guild in guilds:
            check_guild = self.ecdb.check_guild(guild.id)
            if check_guild:
                for member in guild.members:
                    user_check = self.ecdb.check_user(guild, member)
                    if user_check == False:
                        self.ecdb.add_new_user(guild, member)
            else:
                for member in guild.members:
                    self.ecdb.add_new_user(guild, member)

def setup(bot):
    bot.add_cog(Events(bot))