from aiogram import types
from aiogram.filters import CommandObject

import source.keyboards


# Global state for report text (TODO: move to FSM state)
report_text: str | None = None


async def handle_author_report(message: types.Message, command: CommandObject) -> None:
    """Handle /report_author command - create author report for admin."""
    global report_text
    report_text = command.args
    await message.reply(
        'Повідомлення успішно сформовано! Підтвердіть відправку',
        reply_markup=source.keyboards.kb_a_report
    )
