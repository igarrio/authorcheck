from aiogram.filters import Filter
from aiogram.types import Message

import source.database.base


class IsPrivate(Filter):
    """Filter that passes only private chat messages."""

    async def __call__(self, message: Message) -> bool:
        return message.chat.type == 'private'


class UserInBan(Filter):
    """Filter that passes only messages from banned users."""

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in source.database.base.ban_set


class MsgIsMedia(Filter):
    """Filter that passes only photo or video messages."""

    async def __call__(self, message: Message) -> bool:
        content_type = str(message.content_type)
        return content_type in ('ContentType.VIDEO', 'ContentType.PHOTO')