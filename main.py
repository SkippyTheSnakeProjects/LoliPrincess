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
async def on_member_join(member):
    # Welcomes new members
    channel = member.guild.system_channel
    channel = member.guild.channels[0] if channel is None else channel
    await channel.send(f"Hey {member.mention}, welcome to {member.guild.name}")
    utils.log(f"{member.display_name} just joined {member.guild.name}")


@bot.event
async def on_member_remove(member):
    # Load audit logs
    logs = []
    async for log in member.guild.audit_logs():
        logs.append(log)

    # Get the removers member object
    target_id = logs[0].user.id
    for server_member in member.guild.members:
        if server_member.id == target_id:
            remover = server_member

    # Get the channel to send the messages to
    channel = member.guild.system_channel
    channel = member.guild.channels[0] if channel is None else channel

    # Triggers when user is kicked
    if logs[0].action == discord.AuditLogAction.kick:
        await channel.send(
            content = f"Get fucked! {member.mention} has just been KICKED by {remover.mention}:wave::skin-tone-3:")
        utils.log(f"{member.display_name} was just kicked from {member.guild.name} by {remover.display_name}")

    # Triggers when user is banned
    elif logs[0].action == discord.AuditLogAction.ban:
        await channel.send(
            content = f"Get MEGA fucked! {member.mention} has just been BANNED by {remover.display_name} :wave::skin-tone-3:")
        utils.log(f"{member.display_name} was just banned from {member.guild.name} by {remover.display_name}")
    # Any other action is a server leave so send that flavour text
    else:
        await channel.send(
            content = f"{member.mention} has left the server:wave::skin-tone-3:")
        utils.log(f"{member.display_name} has left the server")


@bot.event
async def on_message_edit(before, after):
    # Resubmits and edited message as a command
    await bot.on_message(after)


@bot.event
async def on_command_error(ctx, error):
    # Print the exception to the user
    await ctx.send(f"`{error}`", delete_after = ERROR_DISPLAY_TIME)


log("----- Initializing -----")
# ----- Load all cogs from file
loaded = utils.load_cogs(bot)
log(f"Loaded {loaded} cog{'s' if loaded > 1 else ''}")

# Start bot
bot.run(TOKEN)
