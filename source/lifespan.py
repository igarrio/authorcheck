import asyncio

from source.bot_init import bot, WEBHOOK_URL
from source.utils.bot import get_wh_info, delete_wh, set_wh, close_session
from source.utils.webhook_healthcheck import start_webhook_monitor, stop_webhook_monitor


async def delayed_webhook_monitor():
    await asyncio.sleep(300)
    await start_webhook_monitor(bot, WEBHOOK_URL)


async def on_startup():
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


async def on_shutdown():
    await stop_webhook_monitor()

    _delete_wh = await delete_wh()
    while not _delete_wh:
        _delete_wh = await delete_wh()

    _session_close = await close_session()
    while not _session_close:
        _session_close = await close_session()