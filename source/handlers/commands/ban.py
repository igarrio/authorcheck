import logging

from aiogram import types
from aiogram.filters import CommandObject

import source.config
import source.database.base
from source.database.requests import add_user_id, update_db


async def handle_pidval_sbu(message: types.Message) -> None:
    """Placeholder handler."""
    pass


async def handle_ban(message: types.Message, command: CommandObject) -> None:
    """Handle /ban command - ban user by ID (editors only)."""
    log = logging.getLogger('ban_handle')

    if message.from_user.id not in source.config.editors:
        await message.reply('⛔️ Нажаль, ви не маєте доступу до виконання даної команди ⛔️')
        return

    if command.args is None:
        await message.reply(
            '🗿 Щоб виконати дану команду ви повинні ввести ID користувача, '
            'якому збираєтесь обмежити доступ'
        )
        return

    user_id = int(command.args)
    if user_id in source.database.base.ban_set:
        await message.reply('🕯 Користувач з даним ID вже є заблокованим')
        return

    log.info(f'Ban request to {command.args} by: {message.from_user.id}')
    await add_user_id(user_id, source.database.base.ban_db)
    update_db()
    await message.reply(f'🎉 Користувача з ID <b>{command.args}</b> успішно заблоковано')