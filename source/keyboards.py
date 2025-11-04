from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from source.config import support_url

btn_add_cancel = InlineKeyboardButton(text='❌ Відмінити',
                                      callback_data='cancel_add')

kb_sender = InlineKeyboardMarkup(resize_keyboard=True,
                                 inline_keyboard=[
                                     [InlineKeyboardButton(text='Tак', callback_data=f'start_sender')],
                                     [InlineKeyboardButton(text='Ні', callback_data=f'cancel_sender')]
                                 ]
                                 )

kb_start = InlineKeyboardMarkup(resize_keyboard=True,
                                inline_keyboard=[
                                    [InlineKeyboardButton(text='Автор бота', url='t.me/kimino_musli')],
                                    [InlineKeyboardButton(text='Підтримати', url=support_url)]
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

kb_add = InlineKeyboardMarkup(resize_keyboard=True,
                              inline_keyboard=[
                                  [InlineKeyboardButton(text='Небажаний автор', callback_data='add_bad')],
                                  [InlineKeyboardButton(text='Український автор', callback_data='add_good')]
                              ])

kb_add_confirm = InlineKeyboardMarkup(resize_keyboard=True,
                                          inline_keyboard=[
                                              [InlineKeyboardButton(text='✅ Підтверджую', callback_data='confirm_add')],
                                              [btn_add_cancel]
                                          ])


def generate_sender_keyboard(text, url):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=text,
            url=url
        )
    )
    return builder.as_markup()
