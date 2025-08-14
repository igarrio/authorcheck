import source.keyboards
import source.config
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from source.states.base import SenderMsg
from source.utils.sender import sender_preview

router = Router()


async def handle_sender(message: types.Message, state: FSMContext):
    if message.from_user.id == source.config.admin_id:
        await state.set_state(SenderMsg.text)
        await message.reply('Введіть потрібний вам текст розсилки')
    else:
        await message.reply('⛔️ Дана команда доступна лише адміністратору ⛔️')


async def handle_set_sender_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(SenderMsg.media)
    await message.reply(text='Будь ласка, надішліть фото або відео')


async def handle_set_sender_media(message: types.Message, state: FSMContext):
    _ = f'{message.content_type}'
    if _ == 'ContentType.PHOTO':
        content_id = message.photo[-1].file_id
    elif _ == 'ContentType.VIDEO':
        content_id = message.video.file_id
    await state.update_data(media_type=_)
    await state.update_data(media=content_id)
    await state.set_state(SenderMsg.btn_text)
    await message.reply('Надішлість текст кнопки')


async def handle_set_sender_btn_text(message: types.Message, state: FSMContext):
    await state.update_data(btn_text=message.text)
    await state.set_state(SenderMsg.btn_url)
    await message.reply('Будь ласка, надайте посилання для кнопки')


async def handle_set_sender_btn_url(message: types.Message, state: FSMContext):
    await state.update_data(btn_url=message.text)
    await state.set_state(SenderMsg.btn_url)
    _ = await state.get_data()
    msg_id = await sender_preview(message, _)
    await state.update_data(msg_id=msg_id)
    await message.reply('Повідомлення успішно сформовано! Бажаєте розпочати відправку?',
                        reply_markup=source.keyboards.kb_sender)
    await state.set_state(SenderMsg.confirm)
