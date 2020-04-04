import os
import time
import pytz

import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord import Member
import utils
from datetime import datetime

from config import TIMEZONE


class Discord(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['sc'])
    async def screenshare(self, ctx):
        author = ctx.message.author
        if author.voice is None:
            await ctx.send('You need to be connected to a voice channel to start screen sharing.')
            utils.log(
                f"{ctx.message.author.display_name} requested the screen share link in {ctx.guild.name}")
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

    @commands.command(aliases = ["ms"])
    async def ping(self, ctx):
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)
        await ctx.send(embed = utils.embed(title = "Ping", description = f"Pong {time_delta}ms"))
        utils.log(f"{ctx.message.author.display_name} pinged the server. Ping: {time_delta}ms")

    @commands.command(aliases = ["say", "simonsays"])
    async def echo(self, ctx, *message: str):
        await ctx.send(embed = utils.embed(title = "Echo", description = ' '.join(message)))
        utils.log(f"{ctx.message.author.display_name} echoed \"{' '.join(message)}\"")

    @commands.command(aliases = ["calc"])
    async def math(self, ctx, *equation: str):
        equation = ''.join(equation)
        answer = eval(equation)
        await ctx.send(embed = utils.embed(title = "Math", description = f"`{equation}` = \n{answer}"))
        utils.log(f"{ctx.message.author.display_name} did math equation {equation} = {answer}")

    @commands.command(aliases = ["inv"])
    async def invite(self, ctx):
        try:
            invites = await ctx.guild.invites()
        except discord.Forbidden:
            # The bot needs to have permissions to read invites for this to work
            await ctx.send("I don't have permission to view invites.")
            utils.log(f"{ctx.message.author.display_name} tried to get an invite link for {ctx.guild.name}")
            return

        # Check if a permanent invite is already in place
        perma_invite = None
        for invite in invites:
            if invite.max_uses == invite.max_age == 0:
                perma_invite = invite
                break

        # Create permanent invite if one wasn't found
        if perma_invite is None:
            try:
                perma_invite = await ctx.guild.text_channels[0].create_invite(
                    reason = "Permanent invite for the server")
                utils.log(
                    f"Created a permanent invite for {ctx.guild.name} by request of {ctx.message.author.display_name}")
            except discord.Forbidden:
                # Permission is needed to create invites as well
                await ctx.send("I don't have permission to create invites.")
                utils.log(f"{ctx.message.author.display_name} tried to create an invite link for {ctx.guild.name}")
                return

        # Display the invite link
        utils.log(f"{ctx.message.author.display_name} requested the invite link for {ctx.guild.name}")
        await ctx.send(perma_invite.url)

    @commands.command(aliases = ["t"], hidden = True)
    async def test(self, ctx):
        print(utils.format_time(ctx.message.created_at))


def setup(bot):
    bot.add_cog(Discord(bot))

    # Setup processes
    if not os.path.exists('data/discord'):
        os.mkdir('data/discord')
