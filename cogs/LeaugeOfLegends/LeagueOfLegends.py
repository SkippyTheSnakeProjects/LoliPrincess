from discord import File, Member
from discord.ext import commands
from discord.ext.commands import CommandError
from discord.ext.commands.cog import Cog
from riotwatcher import ApiError

from utils import create_logger


class LeagueOfLegends(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = create_logger(self)
        self.profile_img_path = 'lolProfile.png'

    @commands.command(aliases = ["lolpu"])
    async def lolprofileuser(self, ctx, user: Member = None):
        async with ctx.typing():
            user_id = user.id if user is not None else ctx.author.id
            profile = self.bot.profiles.get_profile_by_id(user_id)
            league_id = profile.league_id
            if league_id is None:
                raise CommandError(
                    f"User {user.mention} doesn't have a League Of Legends id associated with their profile.")

            user = self.bot.lol_watcher.get_lol_profile_by_id(league_id)
            html_content = self.bot.lol_watcher.create_lol_profile_card_html(user)
            path = self.bot.lol_watcher.create_lol_profile_card_img(html_content, self.profile_img_path)
            await ctx.send(file = File(path))

    @commands.command(aliases = ["lolp"])
    async def lolprofile(self, ctx, user: Member = None, lol_username: str = None):
        async with ctx.typing():
            if lol_username is not None:
                user = self.bot.lol_watcher.get_lol_profile_by_name(lol_username)
            elif user is not None:
                profile = self.bot.profiles.get_profile_by_id(user.id)
                user = self.bot.lol_watcher.get_lol_profile_by_id(profile.league_id)

            html_content = self.bot.lol_watcher.create_lol_profile_card_html(user)
            path = self.bot.lol_watcher.create_lol_profile_card_img(html_content, self.profile_img_path)
            await ctx.send(file = File(path))

    @commands.command()
    async def lolmatches(self, ctx, lol_username: str):
        async with ctx.typing():
            try:
                user = self.bot.lol_watcher.summoner.by_name('euw1', lol_username)
            except ApiError as e:
                if e.response.status_code == 429:
                    raise commands.CommandError("Riot servers aren't responding now. Try again later.")
                elif e.response.status_code == 404:
                    raise commands.CommandError(f'No account with name "{lol_username}" found.')
                else:
                    raise

            username = user.get('name')
            profile_icon_id = user.get('profileIconId')

            match_data = self.bot.lol_watcher.match.matchlist_by_account('euw1', profile_icon_id)


def setup(bot):
    bot.add_cog(LeagueOfLegends(bot))
