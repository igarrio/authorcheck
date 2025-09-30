import os
from source.utils.tokens import make_wh_token
from aiogram import Bot, Dispatcher
BOT_TOKEN = os.getenv('bot_api_key')

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()

WEBHOOK_URL = os.getenv("WEBHOOK_URL") + f'/t/{make_wh_token(BOT_TOKEN)}'

async def on_startup():
    from source.database.base import connect_db
    from source.database.requests import update_db
    connect_db()
    update_db()

    from source.handlers.set import set_handlers
    set_handlers()

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
