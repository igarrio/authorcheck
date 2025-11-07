from dash.html import Div, Strong, P
from dash_bootstrap_components import Row


def get_card_obj(data, iso, badge):
    return Div([
        Div([

            Strong(data, className='card-title'),
            ' ',
            badge
            ,
            Row([
                P(f'Last Check: {iso}', className='card-text')
            ]),

        ], className='card-body'),
    ], className='card border-secondary mb-3')
