from dash.html import A
from dash_bootstrap_components import Navbar, Container


header = Navbar(
            Container(
                A(
                    (
                        'AuthorCheck Status Monitor'
                    ), className='d-flex align-items-center my-2 my-lg-0 me-lg-auto text-white text-decoration-none'
                ), className='container-fluid', style={'max-width': '1320px'}
            ), className='navbar navbar-expand-lg bg-primary')