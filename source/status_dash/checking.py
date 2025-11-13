import requests
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import logging

from source.status_dash.res.badges import get_ok_badge, get_error_badge, get_error_badge_for_wh
from source.status_dash.res.check_card import get_card_obj
from source.status_dash.utils import get_iso_kyiv_tz
from source.status_dash.checking_config import dataset
from source.database.base import check_dynamo


dash_check_log = logging.getLogger('DASH MONITOR LOGGING:')

CHECK_CACHE = []
scheduler = BackgroundScheduler()
loop = asyncio.get_event_loop()


async def api(data):
    dash_check_log.warning('Checking API...')
    url = data['custom_request'].get('url')
    headers = data['custom_request'].get('headers', {})
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        badge = get_ok_badge(response.status_code, response.reason)
    else:
        badge = get_error_badge(response.status_code, response.reason)
    return get_card_obj('AuthorCheck Main API ', get_iso_kyiv_tz(), badge)


async def wh(data):
    dash_check_log.warning('Checking Telegram Webhook...')
    url = data['custom_request'].get('url')
    headers = data['custom_request'].get('headers', {})
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        payload = response.json()
        if payload.get('url') == '':
            badge = get_error_badge_for_wh(payload.get('last_error_message'))
        elif payload.get('url') != '':
            badge = get_ok_badge(200, 'ok')
        return get_card_obj('Telegram BOT ', get_iso_kyiv_tz(), badge)


async def db(data):
    dash_check_log.warning('Checking Database...')
    result = check_dynamo()
    if result['success'] is True:
        badge = get_ok_badge(200, 'ok')
    else:
        badge = get_error_badge('error', result['msg'])
    return get_card_obj('Database ', get_iso_kyiv_tz(), badge)


handlers = {
    'api': api,
    'wh': wh,
    'db': db
}

async def run_checks():
    global CHECK_CACHE
    dash_check_log.warning('...Checking started...')
    obj_list = []
    for item in dataset:
        handler = handlers.get(item['id'])
        if handler:
            obj_list.append(await handler(item))
    CHECK_CACHE = obj_list
    dash_check_log.warning('...Checking completed...')


def schedule_run_checks():
    asyncio.run_coroutine_threadsafe(run_checks(), loop)


schedule_run_checks()

scheduler.add_job(schedule_run_checks, 'interval', minutes=15)
scheduler.start()