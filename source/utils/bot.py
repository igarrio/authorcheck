from aiogram.types import WebhookInfo

from source.bot_init import bot, dp, WEBHOOK_URL
from source.utils.tokens import XTBAST


async def run_long_polling() -> None:
    """Start bot in long-polling mode."""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def get_wh_info() -> WebhookInfo:
    """Get current webhook configuration info."""
    return await bot.get_webhook_info()


async def set_wh() -> bool:
    """Configure webhook with secret token."""
    return await bot.set_webhook(
        WEBHOOK_URL,
        drop_pending_updates=True,
        secret_token=XTBAST,
        max_connections=100
    )


async def delete_wh() -> bool:
    """Delete current webhook."""
    return await bot.delete_webhook(drop_pending_updates=True)


async def close_session() -> None:
    """Close bot HTTP session."""
    return await bot.session.close()


async def stop_long_polling() -> None:
    """Stop long-polling mode."""
    await dp.stop_polling()