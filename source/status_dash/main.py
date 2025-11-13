from dash import Dash, Output, Input
from dash.html import Hr, Div
from dash.dcc import Interval
from dash_bootstrap_components import Container, Col
from dash_bootstrap_components.themes import VAPOR
from dash_bootstrap_components.icons import BOOTSTRAP

from source.status_dash.res import footer, header
import source.status_dash.checking as checking

INTERVAL = 900000

status_app = Dash(
    external_stylesheets=[VAPOR, BOOTSTRAP],
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'},
    ],
    name='AuthorCheck Monitor',
    requests_pathname_prefix='/status/',
    use_async=True,
)

status_app.title = 'AuthorCheck Monitor'

status_app.layout = [
    Interval(id='interval', interval=INTERVAL, n_intervals=0),
    header,
    Container([
        Hr(style={'opacity': 0}),
        Container([
            Col(
                Div(id='checks-container', className='mx-auto'), width={'size': 6, 'offset': 3}
            )
        ]),
        footer
    ], style={'max-width': '1320px'}),
]

@status_app.callback(
    Output('checks-container', 'children'),
    Input('interval', 'n_intervals')
)
async def update_check(n):
    return checking.CHECK_CACHE