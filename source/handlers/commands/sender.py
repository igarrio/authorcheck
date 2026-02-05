from aiogram import types
from aiogram.fsm.context import FSMContext

import source.config
import source.keyboards
from source.states.base import SenderMsg
from source.utils.sender import sender_preview


async def handle_sender(message: types.Message, state: FSMContext) -> None:
    """Handle /send command - start broadcast workflow (admin only)."""
    if message.from_user.id != source.config.admin_id:
        await message.reply('⛔️ Дана команда доступна лише адміністратору ⛔️')
        return

    await state.set_state(SenderMsg.text)
    await message.reply('Введіть потрібний вам текст розсилки')


async def handle_set_sender_text(message: types.Message, state: FSMContext) -> None:
    """Handle broadcast text input."""
    await state.update_data(text=message.text)
    await state.set_state(SenderMsg.media)
    await message.reply(text='Будь ласка, надішліть фото або відео')


async def handle_set_sender_media(message: types.Message, state: FSMContext) -> None:
    """Handle broadcast media input."""
    content_type = f'{message.content_type}'

    if content_type == 'ContentType.PHOTO':
        content_id = message.photo[-1].file_id
    elif content_type == 'ContentType.VIDEO':
        content_id = message.video.file_id
    else:
        await message.reply('⛔️ Підтримуються лише фото та відео')
        return

    await state.update_data(media_type=content_type)
    await state.update_data(media=content_id)
    await state.set_state(SenderMsg.btn_text)
    await message.reply('Надішлість текст кнопки')


async def handle_set_sender_btn_text(message: types.Message, state: FSMContext) -> None:
    """Handle broadcast button text input."""
    await state.update_data(btn_text=message.text)
    await state.set_state(SenderMsg.btn_url)
    await message.reply('Будь ласка, надайте посилання для кнопки')


async def handle_set_sender_btn_url(message: types.Message, state: FSMContext) -> None:
    """Handle broadcast button URL input and show preview."""
    await state.update_data(btn_url=message.text)
    data = await state.get_data()
    msg_id, keyboard = await sender_preview(message, data)
    await state.update_data(msg_id=msg_id, keyboard=keyboard)
    await message.reply(
        'Повідомлення успішно сформовано! Бажаєте розпочати відправку?',
        reply_markup=source.keyboards.kb_sender
    )
    await state.set_state(SenderMsg.confirm)
