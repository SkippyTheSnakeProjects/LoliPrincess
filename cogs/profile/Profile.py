from discord import Member
from discord.ext import commands
from discord.ext.commands.cog import Cog

import utils


class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = utils.create_logger(self)

    @commands.command(hidden = "true")
    async def adminpairlolaccount(self, ctx, user: Member, league_name: str):
        self.bot.admins.verify_admin(ctx)
        profile = self.bot.profiles.get_profile_by_id(user.id)
        lol_profile = self.bot.lol_watcher.get_lol_profile_by_name(league_name)
        profile.league_id = str(lol_profile.get('id'))
        self.bot.profiles.save_profiles()

        await ctx.send(embed = utils.embed(title = "Pair lol account",
                                           description = f"Paired {user.mention} with League account:\n"
                                                         f"    Name: {lol_profile.get('name')}\n"
                                                         f"    Id: {lol_profile.get('id')}"))

    @commands.command()
    async def pairlolaccount(self, ctx, league_name: str):
        profile = self.bot.profiles.get_profile_by_id(ctx.author.id)
        lol_profile = self.bot.lol_watcher.get_lol_profile_by_name(league_name)
        profile.league_id = str(lol_profile.get('id'))
        self.bot.profiles.save_profiles()

        await ctx.send(embed = utils.embed(title = "Pair lol account",
                                           description = f"Paired {ctx.author.mention} with League account:\n"
                                                         f"    Name: {lol_profile.get('name')}\n"
                                                         f"    Id: {lol_profile.get('id')}"))


def setup(bot):
    bot.add_cog(Profile(bot))
