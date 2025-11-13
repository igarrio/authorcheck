import logging
from aiogram import types


async def handle_invalid_input(message: types.Message):
    invalid = logging.getLogger('invalid_input')
    _ = f'{message.content_type}'
    invalid.warning(f'{_} by: {message.from_user.url}')
    if _ == 'ContentType.STICKER':
        invalid.warning(f'Sticker URL: https://telegram.me/addstickers/{message.sticker.set_name}')
    elif _ == 'ContentType.TEXT':
        edited_msg = (message.html_text.replace('\n\n', ' ')).replace('\n', '. ')
        invalid.warning(f'Message: {edited_msg}')
