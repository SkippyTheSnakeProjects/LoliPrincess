import os

import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord import Member
import utils


class Admins(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_message_count = 0

    def sent_by_user(self, message_author: discord.Member, from_user: discord.Member):
        is_sent_by_user = from_user is None or str(message_author.id) == str(from_user.id)
        if is_sent_by_user:
            self.deleted_message_count += 1

        return is_sent_by_user

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

    @commands.command()
    async def purge(self, ctx, limit: int, from_user: Member = None):
        await self.bot.admins.verify_admin(ctx)
        self.deleted_message_count = 0

        await ctx.message.channel.purge(limit = min(limit, 100),
                                        check = lambda m: self.sent_by_user(m.author, from_user))

        sent_by_message = f" sent by {from_user.mention}" if from_user is not None else ""
        await ctx.send(embed = utils.embed(
            title = "Purge since",
            description = f"{ctx.message.author.mention} purged {limit} message history"
                          f"{sent_by_message} from {ctx.message.channel.mention}.",
            footer_text = f"Total messages removed: {self.deleted_message_count}"
        ))

    @commands.command()
    async def purgesince(self, ctx, msg: discord.Message, from_user: Member = None):
        await self.bot.admins.verify_admin(ctx)
        self.deleted_message_count = 0
        await ctx.message.channel.purge(limit = 100,
                                        after = msg.created_at,
                                        check = lambda m: self.sent_by_user(m.author, from_user))

        sent_by_message = f" sent by {from_user.mention}" if from_user is not None else ""
        await ctx.send(embed = utils.embed(
            title = "Purge since",
            description = f"{ctx.message.author.mention} purged messages sent since {utils.format_time(msg.created_at)}"
                          f"{sent_by_message} from {ctx.message.channel.mention}.",
            footer_text = f"Total messages removed: {self.deleted_message_count}"
        ))


def setup(bot):
    bot.add_cog(Admins(bot))

    # Setup processes
    if not os.path.exists('data/admin'):
        os.mkdir('data/admin')
