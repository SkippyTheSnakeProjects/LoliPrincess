from discord.ext import commands
from discord.ext.commands.cog import Cog

import utils
from utils import create_logger


class Configuration(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.logger = create_logger(self)

    @commands.command()
    async def reloadProfiles(self, ctx):
        self.bot.admins.verify_admin(ctx)
        self.bot.profiles.load_profiles()
        await ctx.send(embed = utils.embed(title = "Reload profiles",
                                           description = f"Profiles file reloaded."))

    @commands.command()
    async def reloadConfig(self, ctx):
        self.bot.admins.verify_admin(ctx)
        changes = self.bot.config.reload_config()
        changes = f"\n {len(changes)} Change{'s' if len(changes) > 1 else ''}" if len(changes) > 0 else ''
        await ctx.send(embed = utils.embed(title = "Reload config",
                                           description = f"Config file reloaded. {changes}"))

    @commands.command()
    async def setCommandPrefix(self, ctx, new_command_prefix: str):
        self.bot.admins.verify_admin(ctx)
        self.bot.config.CMD_PREFIX = new_command_prefix
        self.bot.config.save_config()
        self.bot.command_prefix = new_command_prefix

        await ctx.send(embed = utils.embed(title = "Set command prefix",
                                           description = f"Set the command prefix to \"{new_command_prefix}\""))

    @commands.command()
    async def setErrorDisplayTime(self, ctx, error_display_time: int):
        self.bot.admins.verify_admin(ctx)
        try:
            self.bot.config.ERROR_DISPLAY_TIME = int(error_display_time)
            self.bot.config.save_config()
        except ValueError:
            raise commands.CommandError("Please enter a valid number.")
        await ctx.send(embed = utils.embed(title = "Set error display time",
                                           description = f"Set the error display time to \"{error_display_time}\""))

    @commands.command()
    async def setTimezone(self, ctx, timezone: str):
        self.bot.admins.verify_admin(ctx)
        self.bot.config.TIMEZONE = timezone
        self.bot.config.save_config()
        await ctx.send(embed = utils.embed(title = "Set timezone",
                                           description = f"Set the timezone to \"{timezone}\""))

    @commands.command()
    async def set(self, ctx):
        self.bot.admins.verify_admin(ctx)


def setup(bot):
    bot.add_cog(Configuration(bot))
