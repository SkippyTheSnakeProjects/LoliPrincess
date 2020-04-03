from discord.ext import commands
from config import CMD_PREFIX, BLACKLISTPATH, ADMINSPATH
import utils
from discord.ext.commands import CommandError


def load_blacklist() -> dict:
    return utils.load_json(BLACKLISTPATH, {})


class Blacklist:
    blacklist = load_blacklist()

    def __init__(self, bot):
        self.bot = bot

    def save_blacklist(self):
        utils.save_json(self.blacklist, BLACKLISTPATH)

    def reload(self):
        self.blacklist = load_blacklist()

    def get_blacklist_for_guild(self, guild_id: str) -> list:
        return self.blacklist.get(str(guild_id), [])

    def add_user_to_blacklist(self, user_id: str, guild_id: str):
        self.blacklist[str(guild_id)] = self.blacklist.get(str(guild_id), []) + [str(user_id)]
        self.save_blacklist()

    def remove_user_from_blacklist(self, user_id: str, guild_id: str):
        self.blacklist[str(guild_id)] = [x for x in self.blacklist.get(str(guild_id)) if x != str(user_id)]
        self.save_blacklist()

    async def is_blacklisted(self, ctx):
        is_blacklisted = str(ctx.author.id) in self.get_blacklist_for_guild(ctx.guild.id)
        if not await self.bot.is_owner(ctx.author) and is_blacklisted:
            raise CommandError("You are blacklisted.")

        return True


def load_admins() -> dict:
    return utils.load_json(ADMINSPATH, {})


class Admins:
    admins = load_admins()

    def __init__(self, bot):
        self.bot = bot

    def save_admins(self):
        utils.save_json(self.admins, ADMINSPATH)

    def reload(self):
        self.admins = load_admins()

    def get_admins_for_guild(self, guild_id: str) -> list:
        return self.admins.get(str(guild_id), [])

    def add_user_to_admins(self, user_id: str, guild_id: str):
        self.admins[str(guild_id)] = self.admins.get(str(guild_id), []) + [str(user_id)]
        self.save_admins()

    def remove_user_from_admins(self, user_id: str, guild_id: str):
        self.admins[str(guild_id)] = [x for x in self.admins.get(str(guild_id)) if x != str(user_id)]
        self.save_admins()

    async def verify_admin(self, ctx):
        is_admin = str(ctx.author.id) in self.get_admins_for_guild(ctx.guild.id)
        if not await self.bot.is_owner(ctx.author) and not is_admin:
            raise CommandError("You need to be an admin to use this command.")

        return True


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(commands.when_mentioned_or(CMD_PREFIX))
        self.blacklist = Blacklist(self)
        self.admins = Admins(self)
