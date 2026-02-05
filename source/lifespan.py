import asyncio

from source.bot_init import bot, WEBHOOK_URL
from source.utils.bot import get_wh_info, delete_wh, set_wh, close_session
from source.utils.webhook_healthcheck import start_webhook_monitor, stop_webhook_monitor


WEBHOOK_MONITOR_DELAY_SECONDS: int = 300


async def delayed_webhook_monitor() -> None:
    """Start webhook monitor after initial delay."""
    await asyncio.sleep(WEBHOOK_MONITOR_DELAY_SECONDS)
    await start_webhook_monitor(bot, WEBHOOK_URL)


async def on_startup() -> None:
    """Application startup: connect DB, set handlers, configure webhook."""
    from source.database.base import connect_db
    from source.database.requests import update_db
    connect_db()
    update_db()

    from source.handlers.set import set_handlers
    set_handlers()

    search_wh = await get_wh_info()
    if search_wh.url != WEBHOOK_URL:
        await delete_wh()
        await set_wh()

    asyncio.create_task(delayed_webhook_monitor())


async def on_shutdown() -> None:
    """Application shutdown: stop monitor, delete webhook, close session."""
    await stop_webhook_monitor()

    delete_success = await delete_wh()
    while not delete_success:
        delete_success = await delete_wh()

    await close_session()