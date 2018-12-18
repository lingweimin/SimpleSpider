from datetime import datetime
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from .config import *


def create_db(database):
    client = MongoClient(DATABASE_URI)
    return client[database or DATABASE_NAME]


db = create_db()


class TableBase:
    _table_name = None

    def add(self, **kwargs):
        new_id = self._query.insert_one(kwargs).inserted_id
        return new_id

    def first(self, **kwargs):
        return self._query.find_one(kwargs)

    def count(self):
        return self._query.count()

    @property
    def _query(self):
        if self._table_name:
            return db[self._table_name]


class Proxy(TableBase):
    _table_name = 'proxy'


class Task(TableBase):
    _table_name = 'task'

    def add(self, task):
        obj = {
            'name': task.name,
            'start_url': task.start_url,
            'status': task.staus
        }
        return super(Task, self).add(**obj)


db.Proxy = Proxy()
db.Task = Task()
