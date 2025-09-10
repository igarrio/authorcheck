import logging

from aiogram import types
from aiogram.filters import CommandObject
from aiogram.exceptions import TelegramNetworkError
from source.database.requests import author_check, get_random_author


async def handle_send_check_result(message: types.Message, command: CommandObject):
    log = logging.getLogger('request')
    log.info(f'Check request: {command.args}\nBy: {message.from_user.url}')

    try:
        if command.args is None:
            await message.reply('❌ Команду введено неправильно. Ось приклад:\n\n<code>/check nickname_or_link</code>')
        elif len(command.args) < 3:
            await message.reply('❌ Команду введено неправильно.\n\nЗдається ваш запит містить менше ніж 3 літери')
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
                good_author = await get_random_author()
                final_message = (f"🙄 Ой йой... Здається я дещо знайшов:\n\n{formatted_results}\n\n"
                                 f"Також радимо ознайомитись з чудовим автором:\n"
                                 f'🌺 <a href="{good_author["link"]}">{good_author["author"]}</a> 🌺')
                await message.reply(final_message)
            else:
                await message.reply('😮‍💨 На щастя - нічого не знайдено!\nАле радимо додатково перевіряти авторів')
    except TelegramNetworkError:
        await message.reply('🥀 🥀 🥀 Вибачте, сталась помилка на стороні серверу Telegram:\n\nTelegramNetworkError: HTTP Client says - Request timeout error')
