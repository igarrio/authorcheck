import time
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import source.database.base
from source.bot_init import bot
from source.utils.sender import start_sending


async def cancel_sender(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Розсилку скасовано')
    await state.clear()
    await callback.answer()


async def start_sender(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_text('Розпочато розсилку')
    await state.clear()
    await callback.answer()

    time_start = time.time()
    count = await start_sending(bot, source.database.base.users_id, callback.message.chat.id, data['msg_id'])
    await callback.message.edit_text(
        f'Було відправлено повідомлень {count} з користувачів {len(source.database.base.users_id)} в базі.'
        f'\n Час: {time.time() - time_start} секунд',
    )


async def handle_add(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'В боті є можливість поповнювати базу небажаних авторів використовуючи команду:\n\n'
        '<i>/add нікнейм_и\n</i>'
        '<i>причина</i>\n\n'
        'Дана функція доступна лише деяким довіреним особам з міркувань безпеки. '
        'Тому якщо ви не є у цьому списку, але бажаєте доповнити базу - звертайтесь до мене, '
        '<a href="t.me/kimino_musli">KimiNo</a>'
    )
