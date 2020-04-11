import os

from discord import Member
from discord.ext import commands
from discord.ext.commands.cog import Cog

import utils
from utils import create_logger


class Blacklist(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = create_logger(self)

    @commands.command()
    async def blacklist(self, ctx):
        blacklist = self.bot.blacklist.get_blacklist_for_guild(ctx.guild.id)
        blacklist = [utils.get_user_from_id(x, ctx.guild).mention for x in blacklist] or ['None']
        await ctx.send(embed = utils.embed(title = 'Blacklist', description = '\n'.join(blacklist)))

    @commands.command()
    async def blacklistadd(self, ctx, member: Member):
        await self.bot.admins.verify_admin(ctx)
        if str(member.id) in self.bot.blacklist.get_blacklist_for_guild(ctx.guild.id):
            raise commands.CommandError(f"{member.mention} is already on the blacklist.")

        self.bot.blacklist.add_user_to_blacklist(member.id, ctx.guild.id)

        await ctx.send(embed = utils.embed(
            title = "Added to blacklist",
            description = f"Added {member.mention} to the blacklist."
        ))

    @commands.command()
    async def blacklistremove(self, ctx, member: Member):
        await self.bot.admins.verify_admin(ctx)
        if str(member.id) not in self.bot.blacklist.get_blacklist_for_guild(ctx.guild.id):
            raise commands.CommandError(f"{member.mention} isn't on the blacklist.")

        self.bot.blacklist.remove_user_from_blacklist(member.id, ctx.guild.id)

        await ctx.send(embed = utils.embed(
            title = "Removed from blacklist",
            description = f"Removed {member.mention} from the blacklist."
        ))

    @commands.command()
    async def reloadblacklist(self, ctx):
        await self.bot.admins.verify_admin(ctx)
        self.bot.blacklist.reload()
        await ctx.send(embed = utils.embed(
            title = "Reload blacklist",
            description = "The blacklist has been reloaded."
        ))


def setup(bot):
    bot.add_cog(Blacklist(bot))

    # Setup processes
    if not os.path.exists('data/admin'):
        os.mkdir('data/admin')
