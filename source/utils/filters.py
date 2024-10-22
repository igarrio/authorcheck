from aiogram.filters import Filter
from aiogram.types import Message
import source.database.base


class IsPrivate(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == 'private'


class UserInBan(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in source.database.base.ban_set


class MsgIsMedia(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == 'ContentType.VIDEO' or 'ContentType.PHOTO'