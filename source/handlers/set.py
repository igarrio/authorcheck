from aiogram import F
from aiogram.filters.command import Command, CommandStart
from source.handlers.callbacks import cancel_sender, start_sender, report_author_confirm, report_bug_confirm, \
    choose_author_add, confirm_add, cancel_add
from source.bot_init import dp
from source.handlers.commands import ban, sender, start, check_result, add, help, report_author, report_bug, inline
from source.handlers.spam_detector import handle_invalid_input
from source.utils.filters import UserInBan, IsPrivate, MsgIsMedia
from source.states.base import SenderMsg, AddMsg

def set_handlers():
    dp.message.register(ban.handle_pidval_sbu, UserInBan(), IsPrivate())
    dp.message.register(start.send_welcome, CommandStart(), IsPrivate())
    dp.message.register(check_result.handle_send_check_result, Command('check', prefix='/'), IsPrivate())
    dp.message.register(ban.handle_ban, Command('ban', prefix='/'), IsPrivate())
    dp.message.register(help.send_help, Command('help', prefix='/'), IsPrivate())

    dp.message.register(sender.handle_sender, Command('send', prefix='/'), IsPrivate())
    dp.message.register(sender.handle_set_sender_text, SenderMsg.text, F.text, IsPrivate())
    dp.message.register(sender.handle_set_sender_media, SenderMsg.media, MsgIsMedia(), IsPrivate())
    dp.message.register(sender.handle_set_sender_btn_text, SenderMsg.btn_text, F.text, IsPrivate())
    dp.message.register(sender.handle_set_sender_btn_url, SenderMsg.btn_url, F.text, IsPrivate())

    dp.message.register(report_author.handle_author_report, Command('report_author', prefix='/'), IsPrivate())
    dp.message.register(report_bug.handle_bug_report, Command('report_bug', prefix='/'), IsPrivate())
    dp.callback_query.register(report_author_confirm, F.data == 'a_report_confirm')
    dp.callback_query.register(report_bug_confirm, F.data == 'b_report_confirm')

    dp.message.register(add.handle_send_add, Command('add', prefix='/'), IsPrivate())
    dp.callback_query.register(choose_author_add, AddMsg.type, F.data.func(lambda data: data == 'add_bad' or data == 'add_good'))
    dp.message.register(add.set_add_arg, AddMsg.content, F.text, IsPrivate())
    dp.callback_query.register(confirm_add, F.data == 'confirm_add')
    dp.callback_query.register(cancel_add, F.data == 'cancel_add')

    dp.callback_query.register(cancel_sender, F.data == 'cancel_sender')
    dp.callback_query.register(start_sender, F.data == 'start_sender', SenderMsg.confirm)

    dp.inline_query.register(inline.ihandler_check)

    dp.message.register(handle_invalid_input, IsPrivate())