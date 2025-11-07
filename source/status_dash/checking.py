import requests
from source.status_dash.res.badges import get_ok_badge, get_error_badge, get_error_badge_for_wh
from source.status_dash.res.check_card import get_card_obj
from source.status_dash.utils import keep_path_only, get_iso_kyiv_tz
from source.database.base import check_dynamo


async def api(data):
    url = data['custom_request'].get('url')
    headers = data['custom_request'].get('headers', {})
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        badge = get_ok_badge(response.status_code, response.reason)
    else:
        badge = get_error_badge(response.status_code, response.reason)
    return get_card_obj(keep_path_only(url), get_iso_kyiv_tz(), badge)


async def wh(data):
    url = data['custom_request'].get('url')
    headers = data['custom_request'].get('headers', {})
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        payload = response.json()
        if payload.get('url') == '':
            badge = get_error_badge_for_wh(payload.get('last_error_message'))
        elif payload.get('url') != '':
            badge = get_ok_badge(200, 'ok')
        return get_card_obj('Telegram BOT', get_iso_kyiv_tz(), badge)


async def db(data):
    result = check_dynamo()
    if result['success'] is True:
        badge = get_ok_badge(200, 'ok')
    else:
        badge = get_error_badge('error', result['msg'])
    return get_card_obj('Database', get_iso_kyiv_tz(), badge)


handlers = {
    'api': api,
    'wh': wh,
    'db': db
}