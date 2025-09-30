import logging
import os
from source.database.config import dynamodb_client


class GetId:
    def __init__(self, database):
        self.database = database

    def get_id(self):
        log = logging.getLogger('get_id')
        response = self.database.scan()
        _ = response.get('Items', [])
        _ = [d['id'] for d in _]
        globals()[self.result] = set(_)
        log.info('DB updated')


class BlacklistId(GetId):
    def __init__(self, database):
        super().__init__(database)
        self.result = 'ban_set'


class UsersId(GetId):
    def __init__(self, database):
        super().__init__(database)
        self.result = 'users_id'


db = None
ban_db = None
users_db = None
good_author_db = None
obj_blacklist = None
obj_users = None
ban_set = None
users_id = None


def connect_db():
    global db
    global ban_db
    global users_db
    global good_author_db
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

