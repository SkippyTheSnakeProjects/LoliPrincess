import os

from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord import Member
import utils


class Admins(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def admins(self, ctx):
        admins = self.bot.admins.get_admins_for_guild(ctx.guild.id)
        admins = [utils.get_user_from_id(x, ctx.guild).mention for x in admins] or ['None']
        await ctx.send(embed = utils.embed(title = 'Admins', description = '\n'.join(admins)))

    @commands.command()
    async def adminsadd(self, ctx, member: Member):
        await self.bot.admins.verify_admin(ctx)
        if str(member.id) in self.bot.admins.get_admins_for_guild(ctx.guild.id):
            raise commands.CommandError(f"{member.mention} is already ad admin.")

        self.bot.admins.add_user_to_admins(member.id, ctx.guild.id)

        await ctx.send(embed = utils.embed(
            title = "Added to admins",
            description = f"{member.mention} is now an admin."
        ))

    @commands.command()
    async def adminsremove(self, ctx, member: Member):
        await self.bot.admins.verify_admin(ctx)
        if str(member.id) not in self.bot.admins.get_admins_for_guild(ctx.guild.id):
            raise commands.CommandError(f"{member.mention} isn't an admin.")

        self.bot.admins.remove_user_from_admins(member.id, ctx.guild.id)

        await ctx.send(embed = utils.embed(
            title = "Removed from admins",
            description = f"Removed admin from {member.mention}."
        ))

    @commands.command()
    async def reloadadmins(self, ctx):
        await self.bot.admins.verify_admin(ctx)
        self.bot.admins.reload()
        await ctx.send(embed = utils.embed(
            title = "Reload admins",
            description = "The admins list has been reloaded."
        ))


def setup(bot):
    bot.add_cog(Admins(bot))

    # Setup processes
    if not os.path.exists('data/admin'):
        os.mkdir('data/admin')
