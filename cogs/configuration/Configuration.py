from discord.ext import commands
from discord.ext.commands.cog import Cog

import utils
from utils import create_logger


class Configuration(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.logger = create_logger(self)

    @commands.command()
    async def setCommandPrefix(self, ctx, new_command_prefix: str):
        await self.bot.admins.verify_admin(ctx)
        self.bot.config.CMD_PREFIX = new_command_prefix
        self.bot.config.save_config()
        self.bot.command_prefix = new_command_prefix

        await ctx.send(embed = utils.embed(title = "Set command prefix",
                                           description = f"Set the command prefix to \"{new_command_prefix}\""))

    @commands.command()
    async def reloadConfig(self, ctx):
        await self.bot.admins.verify_admin(ctx)
        changes = self.bot.config.reload_config()
        changes = f"\n {len(changes)} Change{'s' if len(changes) > 1 else ''}" if len(changes) > 0 else ''
        await ctx.send(embed = utils.embed(title = "Reload config",
                                           description = f"Config file reloaded. {changes}"))


def setup(bot):
    bot.add_cog(Configuration(bot))
