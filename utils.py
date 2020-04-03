import re
from datetime import datetime
import json
from discord.ext.commands.errors import NoEntryPointError
import discord
import os


def log(message: str):
    print(f"{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}  {message}")


def create_filepath(filepath: str):
    if not os.path.exists(filepath):
        os.makedirs(filepath)


def load_json(filepath: str, default_value):
    log(f"Reading file {filepath}")
    # Create the folder for the file to be contained in
    create_filepath(filepath.rsplit('/', 1)[0])

    # Create the file
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump(default_value, f)

    # Read the file
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(data: dict, filepath: str):
    log(f"Saving file {filepath}")
    # Create the folder for the file to be contained in
    create_filepath(filepath.rsplit('/', 1)[0])

    with open(filepath, 'w') as f:
        json.dump(data, f)


def format_time(time):
    """Format time to my preferred display format."""
    return time.strftime("%a, %d %b %Y %I:%M:%S %p")


def load_cogs(bot):
    log("Loading cogs...")
    imported_cogs = 0
    for path, subdirs, files in os.walk('cogs'):
        for name in [x for x in files if x.endswith('.py')]:
            try:
                bot.load_extension(os.path.join(path, name).replace('/', '.').replace('\\', '.')[:-3])
                imported_cogs += 1
                log(f'Loaded {name}')
            except NoEntryPointError:
                pass

    return imported_cogs


def replace(text: str, replacement: dict):
    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in replacement.items())
    # Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


def embed(**kwargs):
    em = discord.Embed(title = kwargs.get('title'),
                       description = kwargs.get('description'))

    em.colour = kwargs.get('colour', 0x1b9c9c)
    em.set_thumbnail(url = kwargs.get('thumbnail', ''))
    em.set_image(url = kwargs.get('image', ''))
    em.set_author(name = kwargs.get('author', ''), url = kwargs.get(
        'author_url', ''), icon_url = kwargs.get('author_icon', ''))
    em.set_footer(text = kwargs.get('footer_text', ''),
                  icon_url = kwargs.get('footer_icon', ''))

    return em


async def send_large_table(channel, table, heading = ''):
    # Split table into 2000 character segments so not to hit the message length limit
    msg = [x + '\n' for x in str(table).split('\n')]
    msg_batch = heading + '\n'
    for i, line in enumerate(msg):
        line = line.lstrip()
        line_added = False

        if len(msg_batch) + len(line) < 1998:
            msg_batch += line
            line_added = True

        else:
            await channel.send(f'`{msg_batch}`')
            msg_batch = ''

        if i == len(msg) - 1 and msg_batch != '':
            await channel.send(f'`{msg_batch}`')
            if not line_added:
                await channel.send(f'`{line}`')


def get_user_from_id(user_id: str, guild: discord.Guild) -> discord.Member:
    if guild is not None:
        for member in guild.members:
            if str(member.id) == str(user_id):
                return member
