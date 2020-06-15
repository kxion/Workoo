import os
import pymysql
from functools import wraps

from utils.log import logger
from utils.run import run_func

from config import DEBUG, MONGO

import pymongo
from copy import copy
from urllib import parse
from datetime import datetime


class MongoOpea(object):
    def __init__(self):
        self.init_mongo()
        super().__init__()

    def init_mongo(self):

        config = MONGO

        config["user"] = parse.quote_plus(config["user"])
        config["passwd"] = parse.quote_plus(config["passwd"])

        client = pymongo.MongoClient(
            "mongodb://{user}:{passwd}@{host}:{port}/".format(**config),
            connect=False)

        self.mongo = client[config.get('basedata')]

    def repeat(self, data, table):
        data = {clean(key): clean(data[key]) for key in data}
        condition = copy(data)
        data['created_at'] = datetime.utcnow()
        result = self.mongo[table].update_one(condition, {'$set': data}, True)

        result_id = result.upserted_id
        if not result_id:
            result_id = self.select(table, condition)

        return result_id

    def insert(self, data, table):
        data['created_at'] = datetime.utcnow()
        if isinstance(data, list):
            result = self.mongo[table].insert_many(data)
            return result.inserted_ids
        else:
            result = self.mongo[table].insert_one(data.copy())
            return result.inserted_id

    def select(self, table, query={}, limit=1, _id=True):
        if limit == 1:
            result = self.mongo[table].find_one(query)
            if _id and result:
                return result.get('_id')
            else:
                return result
        else:
            result = self.mongo[table].find(query).limit(limit)
            return list(result)

    def update(self, query, data, table, multi=False):
        data['updated_at'] = datetime.utcnow()
        if not multi:
            result = self.mongo[table].update_one(query, {'$set': data})
            return result.upserted_id
        else:
            result = self.mongo[table].update_many(query, {'$set': data})
            return result.upserted_ids


def clean(content: str):
    if isinstance(content, str):
        content = content.replace('.', '').replace('\n', '')

    return content
