import os

from aiogram import Bot, Dispatcher

bot = Bot(token=os.environ.get('bot_api_key'), parse_mode='HTML')
dp = Dispatcher()