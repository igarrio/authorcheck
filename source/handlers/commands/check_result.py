import logging

from aiogram import types
from aiogram.filters import CommandObject
from source.database.requests import author_check
from source.utils.links import detect_link
from source.utils.social.pixiv import process_pixiv
from source.utils.social.twitter import extract_author_from_twitter_url


async def handle_send_check_result(message: types.Message, command: CommandObject):
    log = logging.getLogger('request')
    log.info(f'Check request: {command.args}\nBy: {message.from_user.url}')

    if command.args is None:
        await message.reply('❌ Команду введено неправильно. Ось приклад:\n\n/check nickname_or_link')
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
            final_message = f"🙄 Ой йой... Здається я дещо знайшов:\n\n{formatted_results}"
            await message.reply(final_message)
        else:
            await message.reply('😮‍💨 На щастя - нічого не знайдено!\nАле радимо додатково перевіряти авторів')
