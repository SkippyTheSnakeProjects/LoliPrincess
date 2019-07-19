import discord
from discord.ext import commands
from config import CMD_PREFIX, TOKEN
import utils
from utils import log

bot = commands.AutoShardedBot(commands.when_mentioned_or(CMD_PREFIX))


@bot.event
async def on_ready():
    log(f"----- {bot.user.name} online -----")


log("----- Initializing -----")
# ----- Load all cogs from file
loaded = utils.load_cogs(bot)
log(f"Loaded {loaded} cog{'s' if loaded > 1 else ''}")

# Start bot
bot.run(TOKEN)
