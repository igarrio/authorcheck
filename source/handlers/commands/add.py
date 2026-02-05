from aiogram import types
from aiogram.fsm.context import FSMContext

import source.keyboards
from source.config import editors
from source.states.base import AddMsg
from source.utils.add import add_preview


async def handle_send_add(message: types.Message, state: FSMContext) -> None:
    """Handle /add command - start author addition workflow (editors only)."""
    if message.from_user.id not in editors:
        await message.reply('⛔️ Нажаль, ви не маєте доступу до виконання даної команди. ⛔️')
        return

    await state.set_state(AddMsg.type)
    await message.reply(
        'Будь ласка, оберіть те що бажаєте додати',
        reply_markup=source.keyboards.kb_add
    )


async def set_add_arg(message: types.Message, state: FSMContext) -> None:
    """Handle author data input in add workflow."""
    await state.update_data(content=message.text)
    data = await state.get_data()
    try:
        await add_preview(message, data)
    except Exception:
        await message.reply('⛔️ Некоректне введення. Спробуйте спочатку')
        await state.clear()