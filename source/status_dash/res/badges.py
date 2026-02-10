from dash.html import Span


def get_ok_badge(status, reason):
    return Span(
        f'{status} {reason.upper()}',
        className='badge-status badge-ok',
    )


def get_error_badge(status, reason):
    return Span(
        f'{status} {reason.upper()}',
        className='badge-status badge-error',
    )


def get_error_badge_for_wh(error):
    return Span(
        str(error).upper(),
        className='badge-status badge-error',
    )
