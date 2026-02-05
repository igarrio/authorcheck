import asyncio
import logging
from typing import Any, TypedDict

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message, InlineKeyboardMarkup

from source.keyboards import generate_sender_keyboard


log = logging.getLogger('mail_sender')

SEND_DELAY_SECONDS: float = 0.05


class SenderData(TypedDict):
    text: str
    media_type: str
    media: str
    btn_text: str
    btn_url: str


async def sender_preview(message: Message, data: SenderData) -> tuple[int, InlineKeyboardMarkup]:
    """
    Send preview of broadcast message and return message ID with keyboard.
    """
    keyboard = generate_sender_keyboard(data['btn_text'], data['btn_url'])

    if data['media_type'] == 'ContentType.PHOTO':
        send_msg = await message.answer_photo(
            caption=data['text'],
            photo=data['media'],
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    elif data['media_type'] == 'ContentType.VIDEO':
        send_msg = await message.answer_video(
            caption=data['text'],
            video=data['media'],
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    else:
        raise ValueError(f"Unsupported media type: {data['media_type']}")

    return send_msg.message_id, keyboard


async def send_mail(
    bot: Bot,
    to_id: int,
    from_id: int,
    msg_id: int,
    keyboard: InlineKeyboardMarkup
) -> bool:
    """Send single message copy to user with retry on rate limit."""
    try:
        await bot.copy_message(
            chat_id=to_id,
            from_chat_id=from_id,
            message_id=msg_id,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        log.warning(f'Sent msg to {to_id}')
        return True
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_mail(bot, to_id, from_id, msg_id, keyboard)
    except Exception as e:
        log.exception(e)
        return False


async def start_sending(
    bot: Bot,
    to_ids: set[int],
    from_id: int,
    msg_id: int,
    keyboard: InlineKeyboardMarkup
) -> int:
    """Broadcast message to all users and return success count."""
    count = 0
    for user_id in to_ids:
        if await send_mail(bot, user_id, from_id, msg_id, keyboard):
            count += 1
        await asyncio.sleep(SEND_DELAY_SECONDS)
    return count
