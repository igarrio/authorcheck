from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

btn_sender_yes = InlineKeyboardButton(text='Tак', callback_data=f'start_sender')
btn_sender_no = InlineKeyboardButton(text='Ні', callback_data=f'cancel_sender')
kb_sender = InlineKeyboardMarkup(resize_keyboard=True,
                                 inline_keyboard=[
                                     [btn_sender_yes], [btn_sender_no]
                                 ]
                                 )

link = InlineKeyboardButton(text='Автор бота', url='t.me/kimino_musli')
kb_start = InlineKeyboardMarkup(resize_keyboard=True,
                                inline_keyboard=[
                                    [link]
                                ]
                                )

btn_a_report = InlineKeyboardButton(text='✅ Підтверджую', callback_data=f'a_report_confirm')
kb_a_report = InlineKeyboardMarkup(resize_keyboard=True,
                                 inline_keyboard=[[btn_a_report]]
                                 )

btn_b_report = InlineKeyboardButton(text='✅ Підтверджую', callback_data=f'b_report_confirm')
kb_b_report = InlineKeyboardMarkup(resize_keyboard=True,
                                 inline_keyboard=[[btn_b_report]]
                                 )

def generate_sender_keyboard(text, url):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=text,
            url=url
        )
    )
    return builder.as_markup()
