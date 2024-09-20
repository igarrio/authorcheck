from aiogram.types import Message
import source.keyboards


async def add_preview(message: Message, data):
    _ = data['content'].split('\n')
    if len(_) == 2:
        name, info = _[0], _[1]
        if data['type'] == 'add_bad':
            await message.reply('Дані отримано\n\n'
                            f'Небажаний автор: <b>{name}</b>\nПричина: <i>{info}</i>\n\n'
                            '<b>Підтвердити додавання?</b>',
                                reply_markup=source.keyboards.kb_add_confirm)
        elif data['type'] == 'add_good':
            await message.reply('Дані отримано\n\n'
                                f'Український автор: <b>{name}</b>\nПосилання: <i>{info}</i>\n\n'
                                '<b>Підтвердити додавання?</b>',
                                reply_markup=source.keyboards.kb_add_confirm)