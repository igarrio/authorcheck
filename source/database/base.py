import logging
import os
from typing import Any, TypedDict

from source.database.config import dynamodb_client


class DynamoCheckResult(TypedDict):
    success: bool
    msg: str


class GetId:
    """Base class for loading IDs from DynamoDB into memory."""

    result: str  # Name of global variable to populate

    def __init__(self, database: Any) -> None:
        self.database = database

    def get_id(self) -> None:
        log = logging.getLogger('get_id')
        response = self.database.scan()
        items = response.get('Items', [])
        ids = [d['id'] for d in items]
        globals()[self.result] = set(ids)
        log.info('DB updated')


class BlacklistId(GetId):
    """Load banned user IDs into ban_set."""

    def __init__(self, database: Any) -> None:
        super().__init__(database)
        self.result = 'ban_set'


class UsersId(GetId):
    """Load registered user IDs into users_id."""

    def __init__(self, database: Any) -> None:
        super().__init__(database)
        self.result = 'users_id'


# DynamoDB table references
db: Any = None
ban_db: Any = None
users_db: Any = None
good_author_db: Any = None

# In-memory ID sets
ban_set: set[int] | None = None
users_id: set[int] | None = None


def check_dynamo() -> DynamoCheckResult:
    """Check DynamoDB connection status."""
    try:
        main_db = dynamodb_client.Table(os.environ.get('db_name'))
        status = main_db.table_status
        if status == 'ACTIVE':
            return {'success': True, 'msg': 'Main DB Active'}
        return {'success': False, 'msg': f'DB status: {status}'}
    except dynamodb_client.meta.client.exceptions.ResourceNotFoundException:
        return {'success': False, 'msg': 'Error with main DB'}
    except Exception as e:
        return {'success': False, 'msg': str(e)}


def connect_db() -> None:
    """Initialize DynamoDB table connections."""
    global db, ban_db, users_db, good_author_db

    log = logging.getLogger('database')
    log.propagate = False

    db = dynamodb_client.Table(os.environ.get('db_name'))
    log.info(f' MainDB: {db.table_status}')

    ban_db = dynamodb_client.Table(os.environ.get('db_ban'))
    log.info(f' BlackList: {ban_db.table_status}')

    users_db = dynamodb_client.Table(os.environ.get('db_users'))
    log.info(f' UsersDB: {users_db.table_status}')

    good_author_db = dynamodb_client.Table(os.environ.get('db_goodauthor'))
    log.info(f' UaAuthorDB: {good_author_db.table_status}')

