import os
from source.utils.tokens import make_wh_token
from aiogram import Bot, Dispatcher

BOT_TOKEN = os.getenv('bot_api_key')

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()

WEBHOOK_URL = os.getenv("WEBHOOK_URL") + f'/authorcheck/{make_wh_token(BOT_TOKEN)}'

