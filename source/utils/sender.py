import asyncio
import logging
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message
from source.keyboards import generate_sender_keyboard
from source.config import admin_id

log = logging.getLogger('mail_sender')
kb = None


async def sender_preview(message: Message, data):
    global kb
    kb = generate_sender_keyboard(data['btn_text'], data['btn_url'])
    if data['media_type'] == 'ContentType.PHOTO':
        send_msg = await message.answer_photo(caption=data['text'],
                                              photo=data['media'],
                                              reply_markup=kb,
                                              parse_mode='HTML'
                                              )
    elif data['media_type'] == 'ContentType.VIDEO':
        send_msg = await message.answer_video(caption=data['text'],
                                              video=data['media'],
                                              reply_markup=kb,
                                              parse_mode='HTML'
                                              )
    return send_msg.message_id


async def send_mail(bot, to_id, from_id, msg_id):
    try:
        await bot.copy_message(
            chat_id=to_id,
            from_chat_id=from_id,
            message_id=msg_id,
            reply_markup=kb,
            parse_mode='HTML'
        )
        log.info(f'Sended msg to {to_id}')
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_mail(bot, to_id, from_id, msg_id)
    except Exception as e:
        log.info(e)
        return False
    else:
        return True


async def start_sending(bot, to_ids, from_id, msg_id):
    count = 0
    to_ids.remove(admin_id)
    for user_id in to_ids:
        if await send_mail(bot, user_id, from_id, msg_id):
            count += 1
        await asyncio.sleep(0.05)
    return count
