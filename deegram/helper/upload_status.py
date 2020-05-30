import logging
import time

from telethon.errors import MessageNotModifiedError

from ..utils.bot_utils import get_readable_file_size

logger = logging.getLogger(__name__)


class UploadStatus:
    def __init__(self, event, track_count: int = None, total_tracks: int = None):
        self._current = 0
        self._total = 0
        self._event = event
        self._message = None
        self._start_time = 0.0
        self._update_time = 0.0
        self._track_count = track_count
        self._total_tracks = total_tracks

    @property
    def upload_speed(self) -> float:
        return self._current / (time.time() - self._start_time)

    async def start(self) -> None:
        self._start_time = time.time()
        self._message = await self._event.reply("Uploading...")

    async def progress(self, current: int, total: int) -> None:
        self._current = current
        self._total = total
        if (time.time() - self._update_time) > 1:
            msg = ""
            if self._track_count:
                msg += f" 💿 Track {self._track_count} of {self._total_tracks}\n"
            msg += (
                f"🔼 Uploading... {(self._current / self._total):.1%}\n"
                f"⚡ Speed: {get_readable_file_size(self.upload_speed)}/s"
            )
            try:
                await self._message.edit(msg)
            except MessageNotModifiedError:
                logger.debug("Message not modified")
            except ZeroDivisionError:
                logger.debug("Divided zero")
            else:
                self._update_time = time.time()

    async def finished(self) -> None:
        await self._message.delete()
