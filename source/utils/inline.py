from secrets import token_hex
from typing import TypedDict

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent


class AuthorRecord(TypedDict):
    author: str
    description: str


async def build_check_results(
    search: list[AuthorRecord] | None
) -> list[InlineQueryResultArticle]:
    """Build inline query results from database search results."""
    result: list[InlineQueryResultArticle] = []

    if search:
        for item in search:
            result.append(InlineQueryResultArticle(
                id=token_hex(4),
                title=item["author"],
                description=item["description"],
                input_message_content=InputTextMessageContent(
                    message_text=f"<b>{item['author']}</b>\nПричина: <u>{item['description']}</u>"
                )
            ))
    else:
        result = [InlineQueryResultArticle(
            id=token_hex(4),
            title='‍😮‍💨 На щастя - нічого не знайдено!',
            description='Але радимо додатково перевіряти авторів',
            input_message_content=InputTextMessageContent(
                message_text='😮‍💨 На щастя - нічого не знайдено!\nАле радимо додатково перевіряти авторів'
            )
        )]

    return result