from aiogram import Bot

import source.config


async def send_report(
    report_type: str,
    user_id: int,
    bot: Bot,
    name: str,
    text: str
) -> None:
    """Send user report to admin."""
    await bot.send_message(
        chat_id=source.config.admin_id,
        text=f'Повідомлення від <a href="tg://user?id={user_id}">{name}</a> [<code>{user_id}</code>]\nТип: <i>{report_type}</i>\n\n'
             f'{text}',
        parse_mode='HTML'
    )