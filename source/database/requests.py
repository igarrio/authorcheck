import logging
from boto3.dynamodb.conditions import Attr
import source.database.base
from source.utils.request_cleaner import user_request_cleaner


def update_db():
    obj_blacklist = source.database.base.BlacklistId(source.database.base.ban_db)
    obj_users = source.database.base.UsersId(source.database.base.users_db)
    obj_blacklist.get_id()
    obj_users.get_id()


async def author_check(search_name):
    filter_expression = None
    user_request = user_request_cleaner(search_name)
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


async def author_add(name, info):
    source.database.base.db.put_item(
        Item={
            'author': name.lower(),
            'description': info
        }
    )


