import asyncio
import logging
import sys
import configparser
import os
import re
import json
import requests
import boto3
from boto3.dynamodb.conditions import Attr
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

dynamodb_client = boto3.resource(service_name='dynamodb', region_name='eu-central-1',
                                 aws_access_key_id=os.environ.get('aws_access_key_id'),
                                 aws_secret_access_key=os.environ.get('aws_secret_access_key'))

db = dynamodb_client.Table(os.environ.get('db_name'))
print(db.table_status)

add = InlineKeyboardButton(text='Додати автора', callback_data='add')
link = InlineKeyboardButton(text='Автор бота', url='t.me/kimino_musli')
kb_start = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[link], [add]])

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

bot = Bot(token=os.environ.get('bot_api_key'), parse_mode='HTML')
dp = Dispatcher()

ids = cfg['EDITORS']['id']
editors = [int(num.strip()) for num in ids.split(',')]


class PixivDataForParsing:
    url = ''
    meta_count = 0
    link_type = ''
    job_id = ''
    target = ''

    def __init__(self, url, meta_count, link_type, job_id, target):
        self.url = url
        self.meta_count = meta_count
        self.link_type = link_type
        self.job_id = job_id
        self.target = target


async def process_pixiv(user_request):
    id_from_link = (re.search(r'\d+', user_request)).group()
    if 'bookmarks' in user_request:
        pixiv_obj = PixivDataForParsing(f'https://www.pixiv.net/en/users/{id_from_link}', 15, 'user', id_from_link,
                                        'name')
        return await extract_author_from_pixiv_url(pixiv_obj)
    elif 'artworks' in user_request:
        pixiv_obj = PixivDataForParsing(user_request, 26, 'illust', id_from_link, 'userAccount')
        return await extract_author_from_pixiv_url(pixiv_obj)
    elif 'users' in user_request:
        pixiv_obj = PixivDataForParsing(user_request, 15, 'user', id_from_link, 'name')
        return await extract_author_from_pixiv_url(pixiv_obj)
    elif 'illustrations':
        pixiv_obj = PixivDataForParsing(f'https://www.pixiv.net/en/users/{id_from_link}', 15, 'user', id_from_link,
                                        'name')
        return await extract_author_from_pixiv_url(pixiv_obj)


async def extract_author_from_pixiv_url(pixiv_obj):
    response = requests.get(pixiv_obj.url)
    page = BeautifulSoup(response.text, 'html.parser')

    _ = page.find_all('meta')
    meta_tag = (_[pixiv_obj.meta_count])['content']
    data = json.loads(meta_tag)
    return data[pixiv_obj.link_type][pixiv_obj.job_id][pixiv_obj.target]


def user_request_cleaner(text):
    _ = text.replace('__', '')
    _ = (''.join(char for char in _ if not char.isdigit())).lower()

    return _


async def detect_link(text):
    _ = text.split()
    for word in _:
        if word.startswith('https://x.com') or word.startswith('https://twitter.com'):
            return 1
        elif word.startswith('https://www.pixiv.net'):
            return 2
    return 0


async def extract_author_from_twitter_url(url):
    pattern = r'https?://(?:twitter\.com|x\.com)/([^/]+)(?:/status/\d+)?'
    matches = re.findall(pattern, url)

    if matches:
        return matches[0]
    else:
        return None


async def author_add(name, info):
    db.put_item(
        Item={
            'author': name.lower(),
            'description': info
        }
    )


async def author_check(search_name):
    filter_expression = None
    user_request = user_request_cleaner(search_name)
    if filter_expression:
        filter_expression |= Attr('author').contains(user_request)
    else:
        filter_expression = Attr('author').contains(user_request)
    _response = db.scan(
        FilterExpression=filter_expression
    )
    item = _response.get('Items', [])
    if item:
        return item
    else:
        return None


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer(
        '🔬 Хочеш перевірити, чи автор є пов`язаним з агресором?'
        '\nПросто введи:\n\n<b><i>/check нікнейм або посилання Twitter/Pixiv</i></b>'
        '\n\n\n❕ <u><i>нікнейм автора пишемо без "@"</i></u>', reply_markup=kb_start)


@dp.message(Command('check', prefix='/'))
async def send_check_result(message: types.Message, command: CommandObject):
    print(f'Check request: {command.args}')

    if command.args is None:
        await message.reply('❌ Команду введено неправильно. Ось приклад:\n\n<i>/check нік автора бо посилання</i>')
    else:
        if await detect_link(command.args) == 1:
            _ = await extract_author_from_twitter_url(command.args)
        elif await detect_link(command.args) == 2:
            _ = await process_pixiv(command.args)
        elif await detect_link(command.args) == 0:
            _ = command.args
        search = await author_check(_)
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


@dp.message(Command('add', prefix='/'))
async def send_add_russian(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    if user_id in editors:
        print(f'Adding: {command.args} by {user_id}')
        if command.args is None:
            await message.reply('❗ Команда введена некоректно\n\n'
                                'Будь ласка, введіть команду `/add` та два рядки, розділені '
                                'натисканням клавіші Shift+Enter.')
        else:
            lines = command.args.split('\n')
            if len(lines) == 2:
                name, info = lines[0], lines[1]
                await author_add(name, info)
                await message.reply(f'✅ Успішно внесено до бази:\n\nНікнейм: {name}\nПричина: {info}')
            else:
                await message.reply('❗ Команда введена некоректно\n\n'
                                    'Будь ласка, введіть команду `/add` та два рядки, розділені '
                                    'натисканням клавіші Shift+Enter.')
    else:
        await message.reply('⛔️ Нажаль, ви не маєте доступу до виконання даної команди. ⛔️')


@dp.callback_query(lambda c: c.data == 'add')
async def add(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'В боті є можливість поповнювати базу небажаних авторів використовуючи команду:\n\n'
        '<i>/add нікнейм_и\n</i>'
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
