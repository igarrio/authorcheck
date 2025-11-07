import os
from source.utils.tokens import ADMIN_TOKENS

dataset = [
    {
        'id': 'api',
        'custom_request': {
            'url': os.getenv("WEBHOOK_URL") + '/api/healthcheck',
            'headers': {
                'Authorization': f'Bearer {next(iter(ADMIN_TOKENS))}'
            }
        }
    },
    {
        'id': 'wh',
        'custom_request': {
            'url': os.getenv("WEBHOOK_URL") + '/get_webhook_info',
            'headers': {
                'Authorization': f'Bearer {next(iter(ADMIN_TOKENS))}'
            }
        }
    },
    {
        'id': 'db',
        'custom_request': {}
    }
]