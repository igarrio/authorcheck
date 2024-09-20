from secrets import token_hex

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent


async def build_check_results(search):
    result = []
    if search:
        if isinstance(search, list):
            for _ in search:
                result.append(InlineQueryResultArticle(
                    id=token_hex(4),
                    title=f'{_["author"]}',
                    description=f'{_["description"]}',
                    input_message_content=InputTextMessageContent(
                        message_text=f"<b>{_['author']}</b>\nПричина: <u>{_['description']}</u>"
                    )
                ))
        else:
            result.append(InlineQueryResultArticle(
                id=token_hex(4),
                title=f'1. {search["author"]}',
                description=f'{search["description"]}',
                input_message_content=InputTextMessageContent(
                    message_text=f"1. <b>{search['author']}</b>\nПричина: <u>{search['description']}</u>"
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