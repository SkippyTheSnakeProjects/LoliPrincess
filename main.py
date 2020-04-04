import discord
from config import TOKEN
from bot import Bot
import utils
from config import ERROR_DISPLAY_TIME

bot = Bot()


@bot.event
async def on_ready():
    utils.log(f"----- {bot.user.name} online -----")


@bot.event
async def on_member_join(member):
    # Welcomes new members
    channel = member.guild.system_channel or member.guild.channels[0]
    await channel.send(embed = utils.embed(
        title = "User joined!",
        description = f"Hey {member.mention}, welcome to {member.guild.name}!"
    ))
    utils.log(f"{member.display_name} just joined {member.guild.name}")


@bot.event
async def on_guild_remove(member):
    # Get the channel to send the messages to
    default_channel = member.guild.system_channel or member.guild.channels[0]

    # Load audit log
    async for entry in member.guild.audit_logs(limit = 1):
        if entry.target.id == member.id:
            # Triggers when user is kicked
            if entry.action == discord.AuditLogAction.kick:
                await default_channel.send(embed = utils.embed(
                    title = "Kicked!",
                    description = f"Get fucked! {member.mention} has just been KICKED by {entry.user.mention}:wave::skin-tone-3:"
                ))
                utils.log(
                    f"{member.display_name} was just kicked from {member.guild.name} by {entry.user.display_name}")
                return

            # Triggers when user is banned
            elif entry.action == discord.AuditLogAction.ban:
                await default_channel.send(embed = utils.embed(
                    title = "Banned!",
                    description = f"Get MEGA fucked! {member.mention} has just been BANNED by {entry.user.mention} :wave::skin-tone-3:"
                ))

                utils.log(
                    f"{member.display_name} was just banned from {member.guild.name} by {entry.user.display_name}")
                return

    # Any other action is a server leave so send that flavour text
    await default_channel.send(embed = utils.embed(
        title = "Left the server",
        description = f"{member.mention} has left the server:wave::skin-tone-3:"
    ))
    utils.log(f"{member.display_name} has left the server")


@bot.event
async def on_message_edit(before, after):
    # Resubmits and edited message as a command
    await bot.on_message(after)


@bot.event
async def on_command_error(ctx, error):
    # Print the exception to the user
    await ctx.send(embed = utils.embed(title = "Command error", description = f"{error}"),
                   delete_after = ERROR_DISPLAY_TIME)


utils.log("----- Initializing -----")
# ----- Load all cogs from file
loaded = utils.load_cogs(bot)
utils.log(f"Loaded {loaded} cog{'s' if loaded > 1 else ''}")

# ----- Add blacklist check
bot.add_check(bot.blacklist.is_blacklisted)

# Start bot
bot.run(TOKEN)
