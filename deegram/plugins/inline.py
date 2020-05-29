import logging

from telethon import events
from telethon.tl.types import InputWebDocument

from .. import bot
from ..utils.fetch import fetch_json

logger = logging.getLogger(__name__)


@bot.on(events.InlineQuery)
async def inline(event):
    builder = event.builder
    s = []

    if event.text.startswith(".a "):
        album_name = event.text.replace(".a", "").strip()
        if len(album_name) < 1:
            return
        logger.debug(f'Searching for album: {album_name}')
        api_search_link = "https://api.deezer.com/search/album?q=" + album_name

        data = await fetch_json(api_search_link)

        for match in data["data"]:
            s += (
                builder.article(
                    title=match["title"],
                    text=match["link"],
                    description=f"Artist: {match['artist']['name']}\nTracks: {match['nb_tracks']}",
                    thumb=InputWebDocument(
                        url=match["cover_medium"],
                        size=0,
                        mime_type="image/jpeg",
                        attributes=[],
                    ),
                ),
            )

    elif len(event.text) > 1:
        logger.debug(f'Searching for track: {event.text}')
        api_search_link = "https://api.deezer.com/search?q=" + event.text

        data = await fetch_json(api_search_link)

        for match in data["data"]:
            s += (
                builder.article(
                    title=match["title"],
                    text=match["link"],
                    description=f"Artist: {match['artist']['name']}\nAlbum: {match['album']['title']}",
                    thumb=InputWebDocument(
                        url=match["album"]["cover_medium"],
                        size=0,
                        mime_type="image/jpeg",
                        attributes=[],
                    ),
                ),
            )
    if s:
        try:
            await event.answer(s)
        except TypeError:
            pass
