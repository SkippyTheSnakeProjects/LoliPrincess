import os
from pprint import pprint

from discord.ext import commands
from utils import log
from discord.ext.commands.cog import Cog
import cogs.tekken.services as services
from prettytable import PrettyTable
import utils


class Tekken(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['t7md'])
    async def tekkenmovedata(self, ctx, name: str, *move: str):
        log(f"{ctx.message.author.display_name} requested tekken move data for {name} for the move {''.join(move)}")
        # Find matching name
        character_name = services.match_character_name(name)
        if character_name is None:
            raise commands.errors.CommandError(f"Couldn't find a character matching the name \"{name}\"")

        # Get list of matched moves
        move = ' '.join(move)
        move_matches = services.match_move_command(character_name, move)
        if len(move_matches) == 0:
            raise commands.errors.CommandError(f"Couldn't find a move matching the command \"{move}\"")

        # Get all data for the matched moves
        move_data = services.get_move_info(character_name, move_matches)

        # Create table to display information
        table = PrettyTable()
        table.field_names = move_data[0].keys()
        pprint(move_data[0].keys())

        for move in move_data:
            pprint(move.values())
            table.add_row(move.values())

        # This table may be large to use the large table method
        await utils.send_large_table(ctx.message.channel, table, heading = character_name.title())


def setup(bot):
    bot.add_cog(Tekken(bot))

    # Setup processes
    if not os.path.exists('data/tekken'):
        os.mkdir('data/tekken')
