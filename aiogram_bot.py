import asyncio
import logging
import sys
from aiogram import F
from aiogram.filters.command import Command, CommandStart
from source.handlers.callbacks import cancel_sender, start_sender, handle_add
from source.states.base import SenderMsg
from source.database.base import connect_db
import source.database.base
from source.database.requests import update_db
from source.bot_init import bot, dp
from source.handlers.commands import ban, sender, start, check_result, add
from source.handlers.spam_detector import handle_invalid_input


def set_handlers():
    dp.message.register(ban.handle_pidval_sbu, F.from_user.func(lambda from_user: from_user.id in source.database.base.ban_set))
    dp.message.register(start.send_welcome, CommandStart())
    dp.message.register(check_result.handle_send_check_result, Command('check', prefix='/'))
    dp.message.register(ban.handle_ban, Command('ban', prefix='/'))
    dp.message.register(add.handle_send_add_russian, Command('add', prefix='/'))
    dp.callback_query.register(handle_add, F.data == 'add')
    dp.include_router(sender.router)
    dp.callback_query.register(cancel_sender, F.data == 'cancel_sender')
    dp.callback_query.register(start_sender, F.data == 'start_sender', SenderMsg.confirm)
    dp.message.register(handle_invalid_input)


async def main():
    connect_db()
    update_db()
    set_handlers()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
