from aiogram import types
from aiogram.fsm.context import FSMContext
import source.keyboards
from source.config import editors
from source.states.base import AddMsg
from source.utils.add import add_preview


async def handle_send_add(message: types.Message, state: FSMContext):
    await state.set_state(AddMsg.type)
    if message.from_user.id in editors:

        await message.reply('Будь ласка, оберіть те що бажаєте додати',
                            reply_markup=source.keyboards.kb_add)

    else:
        await message.reply('⛔️ Нажаль, ви не маєте доступу до виконання даної команди. ⛔️')


async def set_add_arg(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    _ = await state.get_data()
    try:
        await add_preview(message, _)
    except:
        await message.reply('⛔️ Некоректне введення. Спробуйте спочатку')
        await state.clear()