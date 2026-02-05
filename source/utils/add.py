from typing import TypedDict

from aiogram.types import Message

import source.keyboards


class AddData(TypedDict):
    type: str
    content: str


async def add_preview(message: Message, data: AddData) -> None:
    """Show preview of author data before adding to database."""
    lines = data['content'].split('\n')
    if len(lines) == 2:
        name, info = lines[0], lines[1]
        if data['type'] == 'add_bad':
            await message.reply(
                'Дані отримано\n\n'
                f'Небажаний автор: <b>{name}</b>\nПричина: <i>{info}</i>\n\n'
                '<b>Підтвердити додавання?</b>',
                reply_markup=source.keyboards.kb_add_confirm
            )
        elif data['type'] == 'add_good':
            await message.reply(
                'Дані отримано\n\n'
                f'Український автор: <b>{name}</b>\nПосилання: <i>{info}</i>\n\n'
                '<b>Підтвердити додавання?</b>',
                reply_markup=source.keyboards.kb_add_confirm
            )