import os
from typing import List

import utils

CONFIG_PATH = 'data/config.json'


class Config:

    def __init__(self):
        self._bot = None
        self.TOKEN = ""
        # Define configurable variables
        self.CMD_PREFIX = '?'
        self.ERROR_DISPLAY_TIME = 7
        self.TIMEZONE = 'Europe/London'
        self.LOG_FORMAT = '%(asctime)s [%(name)s] %(message)s'
        self.LOG_LEVEL = 'INFO'

        self.OWNER_ID = 0
        self.BLACKLIST_PATH = 'data/admin/blacklist.json'
        self.ADMINS_PATH = 'data/admin/admins.json'

        self.DISCORD_PROFILE_PATH = "data/discordProfiles.json"

        # If config path doesn't exist create it
        if not os.path.exists(CONFIG_PATH):
            self.save_config()

        # Override default values with values from config
        self.reload_config()

    def save_config(self):
        # Exclude properties that start with and underscore
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        utils.save_json(data, CONFIG_PATH)

    def reload_config(self) -> List[str]:
        config = utils.load_json(CONFIG_PATH, {})
        changed_properties = self.update_from_config_file(config)
        # Update config file to add any missing keys
        self.save_config()

        # Custom actions that need to be performed when loading config
        if self._bot is not None:
            self._bot.command_prefix = self.CMD_PREFIX
            self._bot.blacklist.reload()
            self._bot.admins.reload()

        return changed_properties

    def update_from_config_file(self, config: dict) -> List[str]:
        changed_properties = []
        # Exclude properties that start with and underscore
        for config_property in [x for x in vars(self) if not x.startswith('_')]:
            # Track changed properties
            if config.get(config_property) != getattr(self, config_property):
                changed_properties.append(config_property)

            # Update properties if the key exists in config.json
            if config_property in config.keys():
                setattr(self, config_property, config.get(config_property))

        return changed_properties
