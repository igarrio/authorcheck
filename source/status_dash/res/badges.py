from dash_bootstrap_components import Badge


def get_error_badge(status, reason):
    return Badge(str(status) + ' ' + reason.upper(), color='danger', className='me-1')

def get_ok_badge(status, reason):
    return Badge(str(status) + ' ' + reason.upper(), color='success', className='me-1')

def get_error_badge_for_wh(error):
    return Badge(str(error).upper(), color='danger', className='me-1')