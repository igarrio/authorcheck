import logging
import asyncio
from aiogram.types import Update

feedlog = logging.getLogger('feedUpdate')


async def _feed_update(dp, bot, update: Update, max_retries: int = 5, base_delay: float = 1.5):
    await asyncio.sleep(base_delay)
    attempt = 0
    while True:
        try:
            await dp.feed_update(bot, update)
            return
        except Exception as exc:
            attempt += 1
            feedlog.warning(':feed_update failed on attempt %d: %s', attempt, exc)
            if attempt >= max_retries:
                feedlog.error(':max retries reached for update: %s', exc)
                return
            delay = base_delay * (2 ** (attempt - 1)) + (0.1 * attempt)
            await asyncio.sleep(delay)
