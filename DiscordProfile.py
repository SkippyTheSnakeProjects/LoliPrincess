from typing import Optional

import utils


class DiscordProfile:
    def __init__(self, user_id: str, data: dict = None):
        self.id = user_id

        # Default values
        self.league_id = None

        # Load values from passed data
        for key, value in (data if data is not None else {}).items():
            if hasattr(self, key):
                setattr(self, key, value)


class DiscordProfiles:
    def __init__(self, bot):
        self.bot = bot
        self.profiles = []
        self.load_profiles()

    def load_profiles(self):
        profiles = utils.load_json(self.bot.config.DISCORD_PROFILE_PATH, {'profiles': []}).get('profiles')
        self.profiles = [DiscordProfile(x.get('id'), x) for x in profiles]

    def create_profile(self, user_id: str) -> DiscordProfile:
        user_id = str(user_id)
        # Check if user already exists if so just return that and don't create a new profile
        profile = self.__find_profile_by_id(user_id)
        if profile is not None:
            return profile

        # Create new profile
        new_profile = DiscordProfile(user_id)
        self.profiles.append(new_profile)

        return new_profile

    def __find_profile_by_id(self, user_id: str) -> Optional[DiscordProfile]:
        user_id = str(user_id)
        for profile in self.profiles:
            if profile.id == user_id:
                return profile
        return None

    def get_profile_by_id(self, user_id: str) -> DiscordProfile:
        user_id = str(user_id)
        # Find profile
        profile = self.__find_profile_by_id(user_id)
        if profile is not None:
            return profile

        # Profile not found so create it
        return self.create_profile(user_id)

    def save_profiles(self):
        profiles = [{k: v for k, v in x.__dict__.items()} for x in self.profiles]
        utils.save_json({'profiles': profiles}, self.bot.config.DISCORD_PROFILE_PATH)
