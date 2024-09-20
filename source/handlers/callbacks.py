import time
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import source.database.base
from source.bot_init import bot
from source.database.requests import author_add
from source.states.base import AddMsg
from source.utils.sender import start_sending
from source.utils.report import send_report
import source.handlers.commands.report_author


async def cancel_sender(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Розсилку скасовано')
    await state.clear()
    await callback.answer()


async def cancel_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Додавання відмінено')
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


async def report_author_confirm(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await send_report('Add Author', callback.from_user.id, bot, callback.from_user.first_name, source.handlers.commands.report_author.report_text)
    await callback.message.edit_text('✅ Повідомлення успішно відправлено адміністратору')
    await callback.answer()


async def report_bug_confirm(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await send_report('Bug Report', callback.from_user.id, bot, callback.from_user.first_name, source.handlers.commands.report_bug.report_text)
    await callback.message.edit_text('✅ Повідомлення успішно відправлено адміністратору')
    await callback.answer()


async def choose_author_add(callback: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    await state.update_data(type=callback.data)
    await state.set_state(AddMsg.content)
    if callback.data == 'add_bad':
        await callback.message.edit_text('Ви обрали "Небажаний автор"\n\n'
                                     'Будь ласка, введіть дані в наступному форматі:\n'
                                     '<pre>vasia_pupkin\nVk та Boosty</pre>')
    elif callback.data == 'add_good':
        await callback.message.edit_text('Ви обрали "Український автор"\n\n'
                                         'Будь ласка, введіть дані в наступному форматі:\n'
                                         '<pre>sphenodaile\nhttps://twitter.com/sphenodaile</pre>')


async def choose_good_author_add(callback: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    await state.update_data(type=callback.data)
    await state.set_state(AddMsg.content)
    await callback.message.edit_text('Ви обрали "Український автор"\n\n'
                                     'Будь ласка, введіть дані в наступному форматі:\n'
                                     '<pre>sphenodaile\nhttps://twitter.com/sphenodaile</pre>')


async def confirm_add(callback: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    _ = await state.get_data()
    await author_add(_)
    await callback.message.edit_text('Успішно внесено до бази!')
    await callback.answer()
    await state.clear()


