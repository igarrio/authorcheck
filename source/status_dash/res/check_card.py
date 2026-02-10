from dash.html import Div, Span, P, I


# Map service names to icons & CSS classes
_ICON_MAP = {
    'AuthorCheck Main API ':  ('bi bi-braces',   'icon-api'),
    'Telegram BOT ':          ('bi bi-robot',     'icon-bot'),
    'Database ':              ('bi bi-database',  'icon-db'),
}


def get_card_obj(data, iso, badge):
    icon_class, icon_color = _ICON_MAP.get(data, ('bi bi-check-circle', 'icon-api'))

    return Div([
        Div([
            # Icon
            Div(
                I(className=icon_class),
                className=f'card-icon {icon_color}',
            ),
            # Title + timestamp
            Div([
                Span(data.strip(), className='card-title'),
                P(f'Checked {iso}', className='card-text'),
            ], className='card-info'),
            # Badge
            badge,
        ], className='card-body'),
    ], className='status-card')
