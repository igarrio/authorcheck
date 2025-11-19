from source.bot_init import bot, dp, WEBHOOK_URL
from source.utils.tokens import XTBAST


async def run_long_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def get_wh_info():
    return await bot.get_webhook_info()

async def set_wh():
    return await bot.set_webhook(WEBHOOK_URL,
                              drop_pending_updates=True,
                              secret_token=XTBAST,
                              max_connections=100)

async def delete_wh():
    return await bot.delete_webhook(drop_pending_updates=True)

async def close_session():
    return await bot.session.close()

async def stop_long_polling():
    await dp.stop_polling()