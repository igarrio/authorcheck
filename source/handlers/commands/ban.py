import logging
import source.database.base
import source.config
from aiogram import types
from aiogram.filters import CommandObject
from source.database.requests import add_user_id, update_db


async def handle_pidval_sbu(message: types.Message):
    x = 0


async def handle_ban(message: types.Message, command: CommandObject):
    log = logging.getLogger('ban_handle')
    if message.from_user.id in source.config.editors:
        if command.args is None:
            await message.reply('🗿 Щоб виконати дану команду ви повинні ввести ID користувача, якому збираєтесь '
                                'обмежити доступ')
        elif int(command.args) in source.database.base.ban_set:
            await message.reply(f'🕯 Користувач з даним ID вже є заблокованим')
        else:
            log.info(f'Ban request to {command.args} by: {message.from_user.id}')
            await add_user_id(command.args, source.database.base.ban_db)
            update_db()
            await message.reply(f'🎉 Користувача з ID <b>{command.args}</b> успішно заблоковано')
    else:
        await message.reply('⛔️ Нажаль, ви не маєте доступу до виконання даної команди ⛔️')