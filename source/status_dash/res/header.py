from dash.html import A, Span
from dash_bootstrap_components import Navbar, Container


header = Navbar(
    Container(
        A(
            [
                Span(className='brand-dot'),
                'AuthorCheck Status'
            ],
            className='navbar-brand-text d-flex align-items-center'
        ),
        className='container-fluid',
        style={'max-width': '1320px'}
    ),
    className='status-navbar navbar navbar-expand-lg',
)
