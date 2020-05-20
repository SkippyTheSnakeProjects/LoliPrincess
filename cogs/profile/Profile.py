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

    @commands.command()
    async def karmaRankings(self, ctx):
        karma = {}
        for profile in self.bot.profiles.profiles:
            karma[profile.id] = sum([v for k, v in profile.karma.items() if k != profile.id])
        karma = {k: v for k, v in sorted(karma.items(), key = lambda item: item[1], reverse = True)}

        text = "```\nKarma rankings\n"
        for k, v in karma.items():
            if v == 0:
                continue

            for member in ctx.message.guild.members:
                if str(member.id) == k:
                    text += f'{member.display_name}: {v}\n'

        await ctx.send(text + '\n```')

    @commands.command()
    async def karma(self, ctx, user: Member = None):
        user = ctx.author if user is None else user
        profile = self.bot.profiles.get_profile_by_id(user.id)
        total_karma = 0
        for k, v in profile.karma.items():
            total_karma += v

        await ctx.send(f"{user.display_name}\nKarma: {total_karma}")

    # @commands.command()
    # async def backdateKarma(self, ctx):
    #     if str(ctx.author.id) != "140264216761204737":
    #         return
    #
    #     karma = {}
    #     upvote_id = "393013984892289026"
    #     downvote_id = "393014800197877771"
    #     values = {upvote_id  : 1,
    #               downvote_id: -1}
    #     async for message in ctx.channel.history(limit = None):
    #         print("Processing message")
    #         for reaction in message.reactions:
    #             if not isinstance(reaction.emoji, Emoji):
    #                 continue
    #             # Adding upvotes or downvotes
    #             if str(reaction.emoji.id) in [upvote_id, downvote_id]:
    #                 users = await reaction.users().flatten()
    #                 for user in users:
    #                     users_karma = karma.get(str(message.author.id), {})
    #                     increment = values.get(str(reaction.emoji.id), 0)
    #                     users_karma[str(user.id)] = users_karma.get(str(user.id), 0) + increment
    #                     karma[str(message.author.id)] = users_karma
    #
    #     for k, v in karma.items():
    #         self.bot.profiles.get_profile_by_id(k).karma = v
    #
    #     self.bot.profiles.save_profiles()
    #     print("done")


def setup(bot):
    bot.add_cog(Profile(bot))
