import discord
from discord.ext import commands
from config import CMD_PREFIX, TOKEN
import utils
from utils import log
from config import ERROR_DISPLAY_TIME

bot = commands.AutoShardedBot(commands.when_mentioned_or(CMD_PREFIX))


@bot.event
async def on_ready():
    log(f"----- {bot.user.name} online -----")


@bot.event
async def on_message_edit(before, after):
    # Resubmits and edited message as a command
    await bot.on_message(after)


@bot.event
async def on_command_error(ctx, error):
    # Print the exception to the user
    if isinstance(error, commands.CheckFailure):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(f"`{error}`", delete_after = ERROR_DISPLAY_TIME)


log("----- Initializing -----")
# ----- Load all cogs from file
loaded = utils.load_cogs(bot)
log(f"Loaded {loaded} cog{'s' if loaded > 1 else ''}")

# Start bot
bot.run(TOKEN)
