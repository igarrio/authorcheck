from dash.html import Div, Span, P, I


_ICON_MAP = {
    'Blacklist ':   ('bi bi-slash-circle', 'icon-bot'),
    'Whitelist ':   ('bi bi-patch-check',  'icon-db'),
}


def get_stat_card_obj(label: str, count: int):
    icon_class, icon_color = _ICON_MAP.get(label, ('bi bi-bar-chart', 'icon-api'))

    return Div([
        Div([
            Div(
                I(className=icon_class),
                className=f'card-icon {icon_color}',
            ),
            Div([
                Span(label.strip(), className='card-title'),
                P('Updated every ~6h by AWS', className='card-text'),
            ], className='card-info'),
            Div(str(count), className='badge rounded-pill bg-primary'),
        ], className='card-body'),
    ], className='status-card')