import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Update


feedlog = logging.getLogger('feedUpdate')


async def _feed_update(
    dp: Dispatcher,
    bot: Bot,
    update: Update,
    max_retries: int = 5,
    base_delay: float = 1.5
) -> None:
    """
    Feed update to dispatcher with exponential backoff retry.
    """
    attempt = 0
    while True:
        try:
            await dp.feed_update(bot, update)
            return
        except Exception as e:
            attempt += 1
            feedlog.warning(f':feed_update failed on attempt {attempt}: {e}')
            if attempt >= max_retries:
                feedlog.error(f':max retries reached for update: {e}')
                return
            delay = base_delay * (2 ** (attempt - 1)) + (0.1 * attempt)
            await asyncio.sleep(delay)
