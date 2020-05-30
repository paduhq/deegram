import asyncio
import logging
import time

from telethon.errors import MessageNotModifiedError

from .. import bot
from ..utils.bot_utils import get_readable_file_size

logger = logging.getLogger(__name__)


class DownloadStatus:
    def __init__(self, event):
        self._current = 0
        self._total = 0
        self._event = event
        self._message = None
        self._start_time = 0.0

    @property
    def download_speed(self) -> float:
        return self._current / (time.time() - self._start_time)

    async def start(self) -> None:
        self._message = await self._event.reply("Downloading...")
        self._start_time = time.time()
        bot.loop.create_task(self._on_download_progress())

    async def _on_download_progress(self) -> None:
        while True:
            if self._total and self._total == self._current:
                return
            if self._total:
                try:
                    await self._message.edit(
                        f"🔽 Downloading... {(self._current / self._total):.1%}\n"
                        f"⚡ Speed: {get_readable_file_size(self.download_speed)}/s")
                except MessageNotModifiedError:
                    logger.debug("Message not modified")
                except ZeroDivisionError:
                    logger.debug("Divided zero")
            await asyncio.sleep(1)

    def progress(self, current: int, total: int) -> None:
        self._current = current
        self._total = total

    async def finished(self) -> None:
        await self._message.delete()
