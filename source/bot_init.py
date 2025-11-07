import os
import asyncio
from source.utils.tokens import make_wh_token, XTBAST
from aiogram import Bot, Dispatcher
from source.utils.webhook_healthcheck import start_webhook_monitor, stop_webhook_monitor
BOT_TOKEN = os.getenv('bot_api_key')

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()

WEBHOOK_URL = os.getenv("WEBHOOK_URL") + f'/authorcheck/{make_wh_token(BOT_TOKEN)}'


async def get_webhook_info():
    return await bot.get_webhook_info()


async def on_startup():
    from source.database.base import connect_db
    from source.database.requests import update_db
    connect_db()
    update_db()

    from source.handlers.set import set_handlers
    set_handlers()

    await bot.delete_webhook(drop_pending_updates=True)
    set_result = await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True, secret_token=XTBAST, max_connections=100)
    if not set_result:
        await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True, secret_token=XTBAST, max_connections=100)

    await start_webhook_monitor(bot, WEBHOOK_URL)


async def on_shutdown():
    await stop_webhook_monitor()
    await bot.delete_webhook()
    await bot.session.close()
