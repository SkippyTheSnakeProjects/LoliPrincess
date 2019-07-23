import re
from datetime import datetime
import json
from discord.ext.commands.errors import NoEntryPointError
import discord
import os


def log(message: str):
    print(f"{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}  {message}")


def load_json(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)

    return None


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
            except NoEntryPointError:
                pass

            imported_cogs += 1
            log(f'Loaded {name}')

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
