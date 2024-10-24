from aiogram import types


async def send_help(message: types.Message):
    await message.answer(
        '<b>Як працювати з ботом.</b> <u>Команди:</u>'
        '\n\n'
        "<code>/check</code> — перевірка автора на наявність зв'язків з агресором. Підтримується як псевдонім автора, так і посилання на Twitter/X чи Pixiv."
        "Вводиться в наступних форматах:"
        "\n"
        f"<pre>/check sphenodaile</pre>\n"
        f"<pre>/check https://twitter.com/sphenodaile</pre>"
        f"<pre>/check https://www.pixiv.net/en/users/94080299</pre>"
        "\n\n"
        "<code>/report_author</code> — надіслати адміністратору повідомлення щодо автора_ів, яких бажано додати до бази даних. "
        "На даний момент підтримується лише текст та посилання. Вводиться в наступному форматі:"
        "\n"
        "<pre>/report_author даний автор підтримує агресію проти України. Посилання на автора - x.com/vasia_pupkin</pre>"
        "\n\n"
        "<code>/report_bug</code> — надіслати адміністратору повідомлення при наявності проблем в роботі бота. Формат вводу аналогічний з попередньою командою"
        '\n\n'
        '<b>Inline-mode</b> — режим пошуку з будь якого місця. Просто в полі вводу потрібно ввести текст наступних форматів:\n'
        "<pre>@authorcheck_bot vasia_pupkin</pre>\n"
        "<pre>@authorcheck_bot x.com/vasia_pupkin</pre>"
        "\n\n\n"
        'Також, через те що бот розробляється та підтримується на добровільній основі — буду вдячний за фінансову підтримку.\n'
        'Більше інформації можна отримати на <a href="t.me/kimino_musli">моєму каналі</a>, де я теж буду радий вас бачити, та почути адекватну критику та пропозиції',
        disable_web_page_preview=True)
