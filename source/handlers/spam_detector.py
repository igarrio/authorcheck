import logging

from aiogram import types


async def handle_invalid_input(message: types.Message) -> None:
    """Log invalid/unexpected message types for spam detection."""
    invalid = logging.getLogger('invalid_input')
    content_type = str(message.content_type)
    invalid.warning(f'{content_type} by: {message.from_user.url}')

    if content_type == 'ContentType.STICKER':
        invalid.warning(f'Sticker URL: https://telegram.me/addstickers/{message.sticker.set_name}')
    elif content_type == 'ContentType.TEXT':
        edited_msg = message.html_text.replace('\n\n', ' ').replace('\n', '. ')
        invalid.warning(f'Message: {edited_msg}')
