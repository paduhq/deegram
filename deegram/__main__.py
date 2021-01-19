from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union
    from telethon.tl.patched import Message
    from telethon.events import NewMessage

import shutil
import time

from telethon import Button, events

from . import bot, botStartTime, logger, plugins
from .utils import translate, fetch
from .utils.bot_utils import get_readable_file_size, get_readable_time

plugins.load()

inline_search_buttons = [
    [Button.switch_inline(translate.SEARCH_TRACK, same_peer=True),
     Button.switch_inline(translate.SEARCH_ALBUM, query=".a ", same_peer=True)],
    [Button.inline('❌')]
]


@bot.on(events.NewMessage(pattern='/start'))
async def start(event: Union[NewMessage.Event, Message]):
    await event.reply(translate.WELCOME_MSG, buttons=inline_search_buttons)
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/help'))
async def get_help(event: Union[NewMessage.Event, Message]):
    await event.reply(translate.HELP_MSG)




@bot.on(events.NewMessage(pattern='/source'))
async def info(event: Union[NewMessage.Event, Message]):
    await event.reply(translate.SOURCE_MSG)
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='/info'))
async def info(event: Union[NewMessage.Event, Message]):
    await event.reply(translate.INFO_MSG)
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/log'))
async def log(event: Union[NewMessage.Event, Message]):
    await event.reply(file=f'{__name__}.log')
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/stats'))
async def stats(event: Union[NewMessage.Event, Message]):
    current_time = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    await event.reply(translate.STATS_MSG.format(current_time, total, used, free))
    raise events.StopPropagation


@bot.on(events.NewMessage())
async def search(event: Union[NewMessage.Event, Message]):
    if event.text.startswith('/'):
        search_query = ''
    else:
        search_query = event.text
    await event.respond(translate.CHOOSE, buttons=[
        [Button.switch_inline(translate.SEARCH_TRACK, query=search_query, same_peer=True),
         Button.switch_inline(translate.SEARCH_ALBUM, query=".a " + search_query, same_peer=True)],
        [Button.inline('❌')]
    ])


with bot:
    bot.run_until_disconnected()
    logger.info('Bot stopped')
    bot.loop.run_until_complete(fetch.session.close())
