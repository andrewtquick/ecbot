import discord
import os
import pytz
import time
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
        self.tz = pytz.timezone('America/New_York')
        self.ecdb = DBConnection(self)
        self.utils = Utils(self)

    # On Ready

    @commands.Cog.listener()
    async def on_ready(self):
        event_time = str(dt.now(self.tz))
        parsed_date = self.utils.parse_date_time(event_time)
        print(f'{self.bot.user.name} online.')
        print(f"Current Time: {parsed_date}")
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='.help command'))
        self.gather_all_members()

    # On Member Leave, Kick, and Ban

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        self.O_CHANNEL = self.bot.get_channel(int(self.O_CHAN_GET))
        self.EC_GUILD = self.bot.get_guild(int(self.EC_GUILD_GET))

        async for entry in self.EC_GUILD.audit_logs(limit=1):
            event_time = str(entry.created_at)
            edit_event_time = time.strptime(event_time.split('.')[0], '%Y-%m-%d %H:%M:%S')
            edit_event_time = time.strftime('%m-%d-%Y %I:%M', edit_event_time)
            curr_time = dt.today() + timedelta(hours=4) - timedelta(seconds=1)
            parsed_date = self.utils.parse_date_time(event_time)

            if str(entry.action) == 'AuditLogAction.kick':
                if edit_event_time == curr_time.strftime('%m-%d-%Y %I:%M'):
                    if entry.user.name != 'ECDev' or not entry.user.name != 'Elite Casual Mod':
                        await self.O_CHANNEL.send(f"**{entry.user.name}** kicked **{entry.target.name}** from the server. `Timestamp: {parsed_date}`")
                        user_ref = db.reference('users')
                        member_left = user_ref.child(str(member.id))
                        parsed_date = self.utils.parse_date_time(event_time)
                        member_left.update({
                            'kicked_by': entry.user.name,
                            'kicked_timestamp': parsed_date,
                            'kick_reason': entry.reason})
                        return
            
            if str(entry.action) == 'AuditLogAction.ban':
                if edit_event_time == curr_time.strftime('%m-%d-%Y %I:%M'):
                    if entry.user.name != 'ECDev' or not entry.user.name != 'Elite Casual Mod':
                        await self.O_CHANNEL.send(f"**{entry.user.name}** banned **{entry.target.name}** from the server\nReason: **`{entry.reason}`**\n`Timestamp: {parsed_date}`")
                        user_ref = db.reference('users')
                        member_left = user_ref.child(str(member.id))
                        parsed_date = self.utils.parse_date_time(event_time)
                        member_left.update({
                            'banned_by': entry.user.name,
                            'ban_timestamp': parsed_date,
                            'ban_reason': entry.reason})
                        return

        await self.O_CHANNEL.send(f"**{member.display_name} ({member})** has left the server.`Timestamp: {parsed_date}`")
        user_ref = db.reference('users')
        member_left = user_ref.child(str(member.id))
        member_left.update({'self_leave': str(parsed_date)})

     # On Member Unban

    @commands.Cog.listener()
    async def on_member_unban(self, _, member: Member):
        self.O_CHANNEL = self.bot.get_channel(int(self.O_CHAN_GET))
        self.EC_GUILD = self.bot.get_guild(int(self.EC_GUILD_GET))

        async for entry in self.EC_GUILD.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            event_time = str(entry.created_at)
            parsed_date = self.utils.parse_date_time(event_time)
            await self.O_CHANNEL.send(f"**{entry.user.name}** unbanned **{entry.target}** from the server. `Timestamp: {parsed_date}`")

    # On Member Join Message

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        self.O_CHANNEL = self.bot.get_channel(int(self.O_CHAN_GET))
        event_time = str(dt.now(self.tz))
        parsed_date = self.utils.parse_date_time(event_time)

        await self.O_CHANNEL.send(f"**{member.name}** has joined the server. `Timestamp: {parsed_date}`")
        
        get_embed = self.rules_embed()
        user_check = self.ecdb.check_user(str(member.id))
        if user_check == False:
            self.ecdb.add_new_user(member.id, member, member.name)
            await member.send('https://i.imgur.com/gYeYMCM.png')
            await member.send(embed=get_embed)

        else:
            joined = self.ecdb.get_date(str(member.id))
            minus_week = dt.today() - timedelta(days=7)
            parsed_date = self.utils.parse_date_time(str(minus_week))
            if parsed_date > joined:
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
                event_time = str(entry.created_at)
                parsed_date = self.utils.parse_date_time(event_time)
                if entry.user.name == "ECDev" or entry.user.name == "Elite Casual Mod":
                    pass
                else:
                    await self.O_CHANNEL.send(f"**{entry.user.name}** removed the `{old_role[0].name}` role from **{entry.target.display_name}**. `Timestamp: {parsed_date}`")
        
        if new_role:
            async for entry in self.EC_GUILD.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                event_time = str(entry.created_at)
                parsed_date = self.utils.parse_date_time(event_time)
                if new_role[0].name == 'Server Booster':
                    await self.O_CHANNEL.send(f"**{entry.user.name}** just boosted the server! `Timestamp: {parsed_date}`")
                else:
                    if entry.user.name == "ECDev" or entry.user.name == "Elite Casual Mod":
                        pass
                    else:
                        await self.O_CHANNEL.send(f"**{entry.user.name}** added the `{new_role[0].name}` role to **{entry.target.display_name}**. `Timestamp: {parsed_date}`")

                if new_role[0].name == 'Raider':
                    await entry.target.send(f"Welcome to the Elite Casuals raid team!\n\nPlease take a moment to read the pinned statements in the #announcement channel.\n\nTo access the pins, click the pin icon in the upper right of the channel.\n\nAny questions, please reach out to Xylr, Diamondclaw or Zellah!")


        if before.nick != after.nick:
            user_ref = db.reference('users')
            name_change = user_ref.child(str(before.id))
            check_nick = name_change.get()

            async for entry in self.EC_GUILD.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
                event_time = str(entry.created_at)
                parsed_date = self.utils.parse_date_time(event_time)
                if before.name != entry.user.name:
                    if entry.user.name != "ECDev" or entry.user.name != "Elite Casual Mod":
                        await self.O_CHANNEL.send(f"**{entry.user.name}** changed `{before.name}`'s nickname to **{entry.target.display_name}**. `Timestamp: {parsed_date}`")
                else:
                    await self.O_CHANNEL.send(f"**{before}** changed their nickname to **{entry.target.display_name}** `Timestamp: {parsed_date}`")
                
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
        self.EC_GUILD = self.bot.get_guild(int(self.EC_GUILD_GET))
                
        for member in self.EC_GUILD.members:
            user_check = self.ecdb.check_user(str(member.id))
            if not user_check:
                 self.ecdb.add_new_user(member.id, member, member.name, member.joined_at)


def setup(bot):
    bot.add_cog(Events(bot))