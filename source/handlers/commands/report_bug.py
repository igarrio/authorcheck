import source.keyboards
from aiogram.filters import CommandObject
from aiogram import types

report_text = None


async def handle_bug_report(message: types.Message, command: CommandObject):
    global report_text
    report_text = command.args
    await message.reply('Повідомлення успішно сформовано! Підтвердіть відправку',
                        reply_markup=source.keyboards.kb_b_report)
