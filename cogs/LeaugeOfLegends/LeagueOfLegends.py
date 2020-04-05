from discord import File
from discord.ext import commands
from discord.ext.commands.cog import Cog
from riotwatcher import LolWatcher


class LeagueOfLegends(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lol_watcher = LolWatcher('RGAPI-3b090337-b55f-44ec-9065-f30c7776cf25')

    @commands.command()
    async def lolprofile(self, ctx, lol_username: str):
        user = self.lol_watcher.summoner.by_name('euw1', lol_username)
        username = user.get('name')
        summoner_level = user.get('summonerLevel')
        profile_icon_id = user.get('profileIconId')
        profile_icon = f"https://ddragon.leagueoflegends.com/cdn/10.6.1/img/profileicon/{profile_icon_id}.png"

        ranked_stats = self.lol_watcher.league.by_summoner('euw1', user.get('id'))
        ranked_stats = [x for x in ranked_stats if x.get('queueType') == 'RANKED_SOLO_5x5'][0]

        lp = ranked_stats.get('leaguePoints')
        losses = ranked_stats.get('losses')
        wins = ranked_stats.get('wins')
        tier, rank = ranked_stats.get('tier'), ranked_stats.get('rank')
        rank_txt = f"{tier} {rank}"
        rank_icon = f"https://lolprofile.net/web/img/badges/{rank_txt.replace(' ', '_').upper()}.png"

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
                      <span class="title is-3">{username}</span>
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
                    </div>
                  </div>
                </div>
            
              </div>
            </body>
            
        </html>"""

        self.bot.driver.load_html_content(html_content)
        self.bot.driver.screenshot_element('#main')
        await ctx.send(file = File('screenshot.png'))


def setup(bot):
    bot.add_cog(LeagueOfLegends(bot))
