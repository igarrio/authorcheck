import logging
import random

from boto3.dynamodb.conditions import Attr
import source.database.base
from source.utils.links import detect_link
from source.utils.request_cleaner import user_request_cleaner
from source.utils.social.pixiv import process_pixiv
from source.utils.social.twitter import extract_author_from_twitter_url


def update_db():
    obj_blacklist = source.database.base.BlacklistId(source.database.base.ban_db)
    obj_users = source.database.base.UsersId(source.database.base.users_db)
    obj_blacklist.get_id()
    obj_users.get_id()


async def author_check(arg):
    filter_expression = None
    if await detect_link(arg) == 1:
        _ = await extract_author_from_twitter_url(arg)
    elif await detect_link(arg) == 2:
        _ = await process_pixiv(arg)
    elif await detect_link(arg) == 0:
        _ = arg
    user_request = user_request_cleaner(_)
    if filter_expression:
        filter_expression |= Attr('author').contains(user_request)
    else:
        filter_expression = Attr('author').contains(user_request)
    response = source.database.base.db.scan(
        FilterExpression=filter_expression
    )
    item = response.get('Items', [])
    if item:
        return item
    else:
        return None


async def add_user_id(_, _db):
    _db.put_item(
        Item={
            'id': int(_)
        }
    )


async def author_add(_type: str, _author: str, _data: str ):
    if _type == 'add_good':
        source.database.base.good_author_db.put_item(Item={
        'author': _author.lower(),
        'link': _data
    })
    elif _type == 'add_bad':
        source.database.base.db.put_item(Item={
        'author': _author.lower(),
        'description': _data
    })


async def get_random_author():
    response = source.database.base.good_author_db.scan()
    items = response.get('Items', [])
    random_item = random.choice(items)
    return random_item


