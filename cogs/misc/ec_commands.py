import discord
import discord.utils
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class ECCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Friends and Family Command

    @cog_ext.cog_slash(
        name='ff',
        description='Adds the Friends and Family role to a specific user.',
        guild_ids=[662464939469963285],
        options=[
            create_option(
                name='member',
                description='Select a user',
                required=True,
                option_type=6)
        ])
    async def friends_family(self, ctx: SlashContext, member: str):
        role = discord.utils.get(ctx.guild.roles, name='Friends and Family')
        ochannel = self.bot.get_channel(int(self.OFFICER_CHANNEL))

        if role in member.roles:
            await ctx.send(content=f'{ctx.author.mention} -> **{member.name}** already has that role.', delete_after=60)
        else:
            await member.add_roles(role, atomic=True)
            await ctx.send(content=f'{ctx.author.mention} -> Added `Friends and Family` role to **{member.name}**', delete_after=60)
            await ochannel.send(f"**{ctx.author.name}** added the `Friends and Family` rank to **{member.name}**.")

    # Rules Command

    @cog_ext.cog_slash(
        name='rules',
        description='Displays guild rules.',
        guild_ids=[662464939469963285])
    async def rules(self, ctx: SlashContext):
        await ctx.send(content=f'{ctx.author.mention}\n```📄 Server Rules 📄\n\n❌ No Racism\n❌ No Politics Discussion\n❌ No Toxicity\n❌ No NSFW Content\n✅ Have fun!```\n**These rules are zero tolerance.**')


    # Youtube Channel Command

    @cog_ext.cog_slash(
        name='Youtube',
        description='Link for the Elite Casuals Youtube channel.',
        guild_ids=[662464939469963285]
    )
    async def youtube(self, ctx: SlashContext):
        await ctx.send(f"{ctx.author.mention} -> Here is the Youtube link. https://www.youtube.com/channel/UCWeTRksGtMyXUd_Kn_f-svg")

def setup(bot):
    bot.add_cog(ECCommands(bot))