import os

from discord.ext import commands
from utils import log
from discord.ext.commands.cog import Cog
from discord import Member
import utils


class Discord(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['sc'])
    async def screenshare(self, ctx):
        author = ctx.message.author
        if author.voice is None:
            await ctx.send('You need to be connected to a voice channel to start screen sharing.')
            utils.log(
                f"{ctx.message.author.display_name} requested the screen share link")
        else:
            await ctx.send(f'https://www.discordapp.com/channels/{ctx.guild.id}/{author.voice.channel.id}')
            utils.log(
                f"{ctx.message.author.display_name} requested the screen share link for channel {author.voice.channel.name} in server {author.voice.channel.guild.name}")

    @commands.command()
    async def profile(self, ctx, user: Member = None):
        if user is None:
            user = ctx.author

        em = utils.embed(title = "{} #{}".format(
            user.display_name, user.discriminator), thumbnail = user.avatar_url, colour = user.colour)
        em.add_field(name = "Name", value = user.name)
        em.add_field(name = "Id", value = user.id)
        em.add_field(name = "Created", value = utils.format_time(user.created_at))
        em.add_field(name = "Joined", value = utils.format_time(user.joined_at))
        em.add_field(name = "Status", value = user.status)
        em.add_field(name = "Top role", value = user.top_role)

        if user.activity is not None:
            activity = user.activity.type.name.title()
            activity = activity + ' to' if activity == 'Listening' else activity

            activity_name = user.activity.name

            if activity_name == 'Spotify':
                activity_name += f': {user.activity.title} by {user.activity.artist}'

            em.add_field(name = activity, value = activity_name)

        utils.log(f"{ctx.message.author.display_name} requested {user.display_name}'s profile")
        await ctx.send(embed = em)

    @commands.command(hidden = True)
    async def test(self, ctx, user_id: int):
        user = self.bot.get_user(user_id)
        await ctx.send(user.name)


def setup(bot):
    bot.add_cog(Discord(bot))

    # Setup processes
    if not os.path.exists('data/discord'):
        os.mkdir('data/discord')
