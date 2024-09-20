from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from secrets import token_hex

from source.database.requests import author_check
from source.utils.inline import build_check_results


async def ihandler_check(inline_query: InlineQuery):
    command = inline_query.query
    arg = command.replace('@authorcheckdev_bot ', '')
    try:
        if len(arg) < 3:
            inline_answer = [InlineQueryResultArticle(
                id=token_hex(4),
                title='‍❌ Увага!',
                description='Запит має містити мінімум 3 літери',
                input_message_content=InputTextMessageContent(
                    message_text='❌ Увага!\nЗапит має містити мінімум 3 літери'
                )
            )]
        else:
            search = await author_check(arg)
            inline_answer = await build_check_results(search)

    except Exception as e:
        inline_answer = [InlineQueryResultArticle(
            id=token_hex(4),
            title='‍❌ Виникла помилка!',
            description=f'{e}',
            input_message_content=InputTextMessageContent(
                message_text=f'❌ Виникла помилка!\n\n{e}'
            )
        )]

    await inline_query.answer(inline_answer)