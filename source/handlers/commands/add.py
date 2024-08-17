from aiogram import types
from aiogram.filters import CommandObject
from source.config import editors
from source.database.requests import author_add


async def handle_send_add_russian(message: types.Message, command: CommandObject):
    if message.from_user.id in editors:
        print(f'Adding: {command.args}: by {message.from_user.id}')
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
        await message.reply('⛔️ Нажаль, ви не маєте доступу до виконання даної команди ⛔️')