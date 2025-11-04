from aiogram import types
import source.database.base
from source.database.requests import add_user_id
from source.keyboards import kb_start
from source.config import app_ver


async def send_welcome(message: types.Message):
    if message.from_user.id not in source.database.base.users_id:
        await add_user_id(message.from_user.id, source.database.base.users_db)
        source.database.base.obj_users.get_id()
    await message.answer(
        '🔬 Я - бот, який створений для зручної взаємодії з базою digital-художників, поширення яких є не баженим, '
        "через їх зв'язок з країною-агрессором"
        '\n\nДля початку раджу скористатись командою <code>/help</code>, щоб '
        'запобігти проблем з використанням бота в майбутньому ☝️'
        f'\n\n\nВерсія бота: <b>{app_ver}</b>',
        reply_markup=kb_start)
