import asyncio
import logging
import sys
import configparser
import os
import boto3
from boto3.dynamodb.conditions import Attr

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

dynamodb_client = boto3.resource(service_name='dynamodb', region_name='eu-central-1',
                                 aws_access_key_id=os.environ.get('aws_access_key_id'),
                                 aws_secret_access_key=os.environ.get('aws_secret_access_key'))

db = dynamodb_client.Table(os.environ.get('db_name'))

add = InlineKeyboardButton(text='Додати автора', callback_data='add')
link = InlineKeyboardButton(text='Автор бота', url='t.me/kimino_musli')
kb_start = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[link], [add]])

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

bot = Bot(token=os.environ.get('bot_api_key'), parse_mode='HTML')
dp = Dispatcher()

ids = cfg['EDITORS']['id']
editors = [int(num.strip()) for num in ids.split(',')]


async def author_add(name, info):
    db.put_item(
        Item={
            'author': name,
            'description': info
        }
    )


async def author_check(search_name):
    filter_expression = None
    if filter_expression:
        filter_expression |= Attr('author').contains(search_name)
    else:
        filter_expression = Attr('author').contains(search_name)
    response = db.scan(
        FilterExpression=filter_expression
    )
    item = response.get('Items', [])
    if item:
        return item
    else:
        return None


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer(
        '🔬 Хочеш перевірити, чи автор є пов`язаним з агресором?\nПросто введи:\n\n<b><i>!c нікнейм</i></b>'
        '\n\n\n❕ <u><i>всі команди мають писатися латинськими літерами</i></u>', reply_markup=kb_start)


@dp.message(Command('c', prefix='!'))
async def send_check_result(message: types.Message, command: CommandObject):
    print(f'Check request: {command.args}')

    if command.args is None:
        await message.reply('❌ Команду введено неправильно. Ось приклад:\n\n<i>!с nickname</i>')
    else:
        search = await author_check(command.args)
        if search:
            if isinstance(search, list):
                formatted_results = "\n".join(
                    f"{i + 1}. <b>{result['author']}</b>\nПричина: <u>{result['description']}</u>"
                    for i, result in enumerate(search)
                )
            else:
                formatted_results = "\n".join(
                    f"1. <b>{search['author']}</b>\nПричина: <u>{search['description']}</u>"
                )
            final_message = f'🙄 Ой йой... Здається я дещо знайшов:\n\n{formatted_results}'
            await message.reply(final_message)
        else:
            await message.reply('😮‍💨 На щастя - нічого не знайдено!\nАле радимо додатково перевіряти авторів')


@dp.message(Command('a', prefix='!'))
async def send_add_russian(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    if user_id in editors:
        print(f'Adding: {command.args} by {user_id}')
        if command.args is None:
            await message.reply('❗ Команда введена некоректно\n\n'
                                'Будь ласка, введіть команду `!a` та два рядки, розділені '
                                'натисканням клавіші Shift+Enter.')
        else:
            lines = command.args.split('\n')
            if len(lines) == 2:
                name, info = lines[0], lines[1]
                await author_add(name, info)
                await message.reply(f'✅ Успішно внесено до бази:\n\nНікнейм: {name}\nПричина: {info}')
            else:
                await message.reply('❗ Команда введена некоректно\n\n'
                                    'Будь ласка, введіть команду `!a` та два рядки, розділені '
                                    'натисканням клавіші Enter.')
    else:
        await message.reply('⛔️ Нажаль, ви не маєте доступу до виконання даної команди. ⛔️')


@dp.callback_query(lambda c: c.data == 'add')
async def add(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'В боті є можливість поповнювати базу небажаних авторів використовуючи команду:\n\n'
        '<i>!a нікнейм_и\n</i>'
        '<i>причина</i>\n\n'
        'Дана функція доступна лише деяким довіреним особам з міркувань безпеки. '
        'Тому якщо ви не є у цьому списку, але бажаєте доповнити базу - звертайтесь до мене, '
        '<a href="t.me/kimino_musli">KimiNo</a>'
    )


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
