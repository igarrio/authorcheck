from dash.html import I, Div
from dash_bootstrap_components import CardFooter, Row, ListGroup, ListGroupItem, Stack

from source.config import support_url


footer = CardFooter(
    Row(
        [
            Stack([
                Div([
                    ListGroup([
                        ListGroupItem([I(className='bi bi-telegram'), ' Telegram'], external_link=True, href='https://t.me/kimino_musli', className='bg-transparent'),
                        ListGroupItem([I(className='bi bi-telegram'), ' Donate'], external_link=True, href=support_url, className='bg-transparent')
                        ], horizontal=True, flush=True)
                    ], className='mx-auto'
                )
            ], direction='horizontal', gap=3),

        ]
    )
)