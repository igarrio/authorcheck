import random
from typing import Any, TypedDict

from boto3.dynamodb.conditions import Attr

import source.database.base
from source.utils.links import detect_link
from source.utils.request_cleaner import user_request_cleaner
from source.utils.social.pixiv import process_pixiv
from source.utils.social.twitter import extract_author_from_twitter_url


class AuthorRecord(TypedDict):
    author: str
    description: str


class GoodAuthorRecord(TypedDict):
    author: str
    link: str


def update_db() -> None:
    """Refresh in-memory ID sets from DynamoDB."""
    obj_blacklist = source.database.base.BlacklistId(source.database.base.ban_db)
    obj_users = source.database.base.UsersId(source.database.base.users_db)
    obj_blacklist.get_id()
    obj_users.get_id()


async def author_check(arg: str) -> list[AuthorRecord] | None:
    """
    Search for author in blacklist database.
    Supports direct nicknames, Twitter/X URLs, and Pixiv URLs.
    """
    link_type = await detect_link(arg)

    if link_type == 1:
        author_name = await extract_author_from_twitter_url(arg)
    elif link_type == 2:
        author_name = await process_pixiv(arg)
    else:
        author_name = arg

    if not author_name:
        return None

    user_request = user_request_cleaner(author_name)
    filter_expression = Attr('author').contains(user_request)

    response = source.database.base.db.scan(
        FilterExpression=filter_expression
    )
    items = response.get('Items', [])

    return items if items else None


async def add_user_id(user_id: int, database: Any) -> None:
    """Add new user ID to database."""
    database.put_item(
        Item={
            'id': int(user_id)
        }
    )


async def author_add(author_type: str, author: str, data: str) -> None:
    """
    Add author to database.

    Args:
        author_type: 'add_good' for Ukrainian authors, 'add_bad' for blacklist
        author: Author nickname
        data: Link (for good) or reason (for bad)
    """
    if author_type == 'add_good':
        source.database.base.good_author_db.put_item(
            Item={
                'author': author.lower(),
                'link': data
            }
        )
    elif author_type == 'add_bad':
        source.database.base.db.put_item(
            Item={
                'author': author.lower(),
                'description': data
            }
        )


async def get_random_author() -> GoodAuthorRecord:
    """Get random Ukrainian author from database."""
    response = source.database.base.good_author_db.scan()
    items = response.get('Items', [])
    return random.choice(items)


