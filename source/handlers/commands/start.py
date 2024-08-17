from aiogram import types
import source.database.base
from source.database.requests import add_user_id
from source.keyboards import kb_start


async def send_welcome(message: types.Message):
    if message.from_user.id not in source.database.base.users_id:
        await add_user_id(message.from_user.id, source.database.base.users_db)
        source.database.base.obj_users.get_id()
    await message.answer(
        '🔬 Хочеш перевірити, чи автор є пов`язаним з агресором?'
        '\nПросто введи:\n\n<b><i>/check нікнейм або посилання Twitter/Pixiv</i></b>'
        '\n\n\n❕ <u><i>нікнейм автора пишемо без "@"</i></u>', reply_markup=kb_start)
