from discord.ext import commands
from riotwatcher import ApiError, LolWatcher as LolWatcherOriginal

import utils


class LolWatcher(LolWatcherOriginal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(self.bot.config.LOL_API_KEY)
        self.logger = utils.create_logger(self)

    def get_lol_profile_by_name(self, username: str):
        try:
            return self.summoner.by_name('euw1', username)
        except ApiError as e:
            if e.response.status_code == 429:
                raise commands.CommandError("Riot servers aren't responding now. Try again later.")
            elif e.response.status_code == 404:
                raise commands.CommandError(f'No account with name "{username}" found.')
            else:
                raise

    def get_lol_profile_by_id(self, user_id: str):
        try:
            return self.summoner.by_id('euw1', user_id)
        except ApiError as e:
            if e.response.status_code == 429:
                raise commands.CommandError("Riot servers aren't responding now. Try again later.")
            elif e.response.status_code == 404:
                raise commands.CommandError(f'No account with id "{user_id}" found.')
            else:
                raise

    def create_lol_profile_card_html(self, user: dict):
        # Extract info from user
        username = user.get('name')
        summoner_level = user.get('summonerLevel')
        profile_icon_id = user.get('profileIconId')
        profile_icon = f"https://ddragon.leagueoflegends.com/cdn/10.6.1/img/profileicon/{profile_icon_id}.png"

        # Get ranked stats
        ranked_stats = self.league.by_summoner('euw1', user.get('id'))
        ranked_stats = [x for x in ranked_stats if x.get('queueType') == 'RANKED_SOLO_5x5']
        if len(ranked_stats) == 0:
            raise commands.CommandError(f'There are no ranked matches found for "{username}".')

        # Extract info from ranked stats
        ranked_stats = ranked_stats[0]
        lp = ranked_stats.get('leaguePoints')
        losses = ranked_stats.get('losses')
        wins = ranked_stats.get('wins')
        tier, rank = ranked_stats.get('tier'), ranked_stats.get('rank')
        rank_txt = f"{tier} {rank}"
        rank_icon = f"https://lolprofile.net/web/img/badges/{rank_txt.replace(' ', '_').upper()}.png"
        veteran = ranked_stats.get('veteran')

        html_content = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                      <meta charset="UTF-8">
                      <meta name="viewport" content="width=device-width, initial-scale=1.0">
                      <title>Document</title>
                      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.1/css/bulma.min.css">
                      <style>
                        .card {
                          /* Base colour */
                          background-color: rgb(40, 44, 52);
                          /* Base text colour */
                          color: rgb(220, 221, 222);
                        }

                        .card-content {
                          padding-bottom: 0px;
                        }

                        .title-container {
                          padding: 10px;
                          padding-left: 20px;
                          /* Darkest accent colour */
                          border-bottom: solid rgb(23, 25, 29);
                          /* Darker base colour */
                          background-color: rgb(33, 37, 43);
                        }

                        .title {
                          color: rgb(220, 221, 222);
                        }

                        .veteran {
                          color: rgb(255, 215, 0);
                        }

                        .win-txt {
                          color: rgb(113, 255, 190);
                        }

                        .lose-txt {
                          color: rgb(255, 113, 113);
                        }
                      </style>
                    </head>"""

        html_content += f"""
                        <body style="max-width: 400px; max-height: 500px;">
                          <div class="card" id="main">
                            <div class="title-container">
                              <div class="columns">
                                <div class="column" style="max-width: 100px; padding-left: 0px; padding-bottom: 8px;">
                                  <img src="{profile_icon}" alt="Placeholder image"
                                    height="100" width="100" style="border-radius: 10px;">
                                </div>
                                <div class="column" style="padding-left: 0px;">
                                  <span class="title is-3 {'veteran' if veteran else ''}">{username}</span>
                                  <br>
                                  <span>EU WEST (euw)</span>
                                  <br>
                                  <span>Level {summoner_level}</span>
                                </div>
                              </div>
                            </div>

                            <div class="card-content">
                              <div class="media">
                                <div class="media-left">
                                  <figure class="image" style="margin-left: -20px; margin-top: -35px;">
                                    <img src="{rank_icon}" alt="Placeholder image">
                                  </figure>
                                </div>
                                <div style="margin-left: -20px; margin-top: 10px;">
                                  <span class="title is-5">{rank_txt}</span>
                                  <br>
                                  <span>{lp} LP</span>
                                  <br>
                                  <span class="win-txt">{wins} Wins</span>
                                  <span class="lose-txt">{losses} Losses</span>
                                  <br>
                                  <span>{(wins / (wins + losses)) * 100:.2f}%</span>
                                </div>
                              </div>
                            </div>

                          </div>
                        </body>

                    </html>"""
        return html_content

    def create_lol_profile_card_img(self, html_content: str, filepath: str):
        self.bot.driver.load_html_content(html_content)
        self.bot.driver.screenshot_element('#main', filepath)
        return filepath
