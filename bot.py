import logging
from io import BytesIO

import coloredlogs
from PIL import Image
from discord.ext import commands
from discord.ext.commands import CommandError

import utils
from DiscordProfile import DiscordProfiles
from config import Config


class Blacklist:
    def __init__(self, bot):
        self.bot = bot
        self.blacklist = None

    def load_blacklist(self) -> dict:
        return utils.load_json(self.bot.config.BLACKLIST_PATH, {})

    def save_blacklist(self):
        utils.save_json(self.blacklist, self.bot.config.BLACKLIST_PATH)

    def reload(self):
        self.blacklist = self.load_blacklist()

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


class Admins:
    def __init__(self, bot):
        self.bot = bot
        self.admins = None

    def load_admins(self) -> dict:
        return utils.load_json(self.bot.config.ADMINS_PATH, {})

    def save_admins(self):
        utils.save_json(self.admins, self.bot.config.ADMINS_PATH)

    def reload(self):
        self.admins = self.load_admins()

    def get_admins_for_guild(self, guild_id: str) -> list:
        return self.admins.get(str(guild_id), [])

    def add_user_to_admins(self, user_id: str, guild_id: str):
        self.admins[str(guild_id)] = self.admins.get(str(guild_id), []) + [str(user_id)]
        self.save_admins()

    def remove_user_from_admins(self, user_id: str, guild_id: str):
        self.admins[str(guild_id)] = [x for x in self.admins.get(str(guild_id)) if x != str(user_id)]
        self.save_admins()

    def verify_admin(self, ctx):
        is_admin = str(ctx.author.id) in self.get_admins_for_guild(ctx.guild.id)
        if not str(ctx.author.id) == str(self.bot.config.OWNER_ID) and not is_admin:
            raise CommandError("You need to be an admin to use this command.")

        return True

class Bot(commands.AutoShardedBot):
    def __init__(self):
        self.config = Config()
        super().__init__(commands.when_mentioned_or(''))
        self.blacklist = Blacklist(self)
        self.admins = Admins(self)
        self.profiles = DiscordProfiles(self)
