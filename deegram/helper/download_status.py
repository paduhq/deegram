import asyncio
import logging
import time

from telethon.errors import MessageNotModifiedError

from .. import bot
from ..utils.bot_utils import get_readable_file_size

logger = logging.getLogger(__name__)


class DownloadStatus:
    def __init__(self, event):
        self.current = 0
        self.total = 0
        self.event = event
        self._start_time = 0.0

    @property
    def download_speed(self):
        return self.current / (time.time() - self._start_time)

    async def start(self):
        self.message = await self.event.reply("Downloading...")
        self._start_time = time.time()
        bot.loop.create_task(self._on_download_progress())

    async def _on_download_progress(self):
        while True:
            if self.total and self.total == self.current:
                return
            if self.total:
                try:
                    await self.message.edit(
                        f"Downloading... {(self.current / self.total):.1%}\n"
                        f"Speed: {get_readable_file_size(self.download_speed)}/s")
                except MessageNotModifiedError:
                    logger.debug("Message not modified")
                except ZeroDivisionError:
                    logger.debug("Divided zero")
            await asyncio.sleep(1)

    def progress(self, current, total):
        self.current = current
        self.total = total

    async def finished(self):
        await self.message.delete()
