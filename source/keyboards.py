from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from source.config import support_url


btn_add_cancel: InlineKeyboardButton = InlineKeyboardButton(
    text='❌ Відмінити',
    callback_data='cancel_add'
)

kb_sender: InlineKeyboardMarkup = InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[
        [InlineKeyboardButton(text='Tак', callback_data='start_sender')],
        [InlineKeyboardButton(text='Ні', callback_data='cancel_sender')]
    ]
)

kb_start: InlineKeyboardMarkup = InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[
        [InlineKeyboardButton(text='Автор бота', url='t.me/kimino_musli')],
        [InlineKeyboardButton(text='Підтримати', url=support_url)]
    ]
)

btn_a_report: InlineKeyboardButton = InlineKeyboardButton(
    text='✅ Підтверджую',
    callback_data='a_report_confirm'
)
kb_a_report: InlineKeyboardMarkup = InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[[btn_a_report]]
)

btn_b_report: InlineKeyboardButton = InlineKeyboardButton(
    text='✅ Підтверджую',
    callback_data='b_report_confirm'
)
kb_b_report: InlineKeyboardMarkup = InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[[btn_b_report]]
)

kb_add: InlineKeyboardMarkup = InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[
        [InlineKeyboardButton(text='Небажаний автор', callback_data='add_bad')],
        [InlineKeyboardButton(text='Український автор', callback_data='add_good')]
    ]
)

kb_add_confirm: InlineKeyboardMarkup = InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[
        [InlineKeyboardButton(text='✅ Підтверджую', callback_data='confirm_add')],
        [btn_add_cancel]
    ]
)


def generate_sender_keyboard(text: str, url: str) -> InlineKeyboardMarkup:
    """Generate inline keyboard with single button."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=text,
            url=url
        )
    )
    return builder.as_markup()
