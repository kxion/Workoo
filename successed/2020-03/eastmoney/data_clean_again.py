import os
import re
import json
import bson
import pymysql
import pymongo
import datetime
from urllib import parse
from pymongo import MongoClient
from config import DEBUG, logger, MONGO


def init_mongo():

    if DEBUG:
        config = MONGO["debug"]
    else:
        config = MONGO["product"]

    config["user"] = parse.quote_plus(config["user"])
    config["passwd"] = parse.quote_plus(config["passwd"])

    client = MongoClient(
        "mongodb://{user}:{passwd}@{host}:{port}/".format(**config))

    return client["eastmoney"]


def init_mysql():
    from config import DATABASES

    try:
        if DEBUG:
            config = DATABASES["debug"]
        else:
            config = DATABASES["product"]

        ecnu_mysql = pymysql.connect(**config)

    except pymysql.err.OperationalError as exc:
        logger.error("--->Error: 登录失败！TimeoutError!")
        os._exit(0)
    else:
        return ecnu_mysql.cursor()


class DataClean(object):
    def get_date(self):
        # date_temp = datetime.datetime.strptime(
        #     self.date, "%Y-%m-%d") + datetime.timedelta(days=-1)
        date_temp = self.date + datetime.timedelta(days=-1)
        if date_temp.month <= 7 and date_temp.year <= 2018:
            return False
        else:
            self.last_date = self.date
            # self.date = date_temp.strftime("%Y-%m-%d")
            self.date = date_temp

            return True

    def get_guba(self):
        with open('./lack.json', 'r', encoding='utf-8') as fn:
            gubas = json.loads(fn.read())

        for guba in gubas:
            yield guba

    def get_count(self):
        data = []
        while True:
            if self.get_date() is True:
                result = mongo['comment'].count_documents({
                    '$and': [{
                        "GubaId": self.guba
                    }, {
                        "post_time": {
                            '$gt': self.date
                        }
                    }, {
                        "post_time": {
                            '$lte': self.last_date
                        }
                    }]
                })

                info = {
                    'GubaId': self.guba,
                    'Date': self.last_date,
                    'Count': result
                }
                data.append(info)
            else:
                break

        mongo['count'].insert_many(data)

    def get_all(self):
        result = list(mongo['comment'].find({"GubaId": self.guba}))

        result = [
            x for x in result if datetime.datetime.strptime(
                '2018-07-01 15:00:00', '%Y-%m-%d  %H:%M:%S') <=
            x['post_time'] <= datetime.datetime.strptime(
                '2019-08-01 15:00:00', '%Y-%m-%d  %H:%M:%S')
        ]

        info = []
        while True:
            count = 0
            if self.get_date() is True:
                data = []
                for index, value in enumerate(result):
                    if value['post_time'] <= self.last_date and value[
                            'post_time'] > self.date:
                        count += 1
                        data.append(value)

                for value in data:
                    result.remove(value)

                info.append({
                    'GubaId': self.guba,
                    'Date': self.last_date,
                    'Count': count
                })
            else:
                break

        mongo['count'].insert_many(info)

    def main(self):
        yield_guba = self.get_guba()

        while True:
            self.date = datetime.datetime.strptime('2019-08-01 15:00:00',
                                                   '%Y-%m-%d  %H:%M:%S')

            try:
                self.guba = next(yield_guba)
            except StopIteration:
                break
            else:
                self.get_all()
                logger.info("Info: the {} is done".format(self.guba))

        logger.info("success")


def clean_date():
    pattern = re.compile(r'\s+$')
    regex = bson.regex.Regex.from_native(pattern)
    regex.flags ^= re.UNICODE

    # 'post_time': regex 正则
    # 'post_time': { '$type': 2 } Sting 类型
    result = list(mongo['comment'].find({'post_time': regex}))

    for data in result:
        data['post_time'] = datetime.datetime.strptime(
            data['post_time'].strip(' '), "%Y-%m-%d %H:%M:%S")
        mongo['comment'].update_one({'_id': data['_id']}, {'$set': data})
        print('down')


def unify_data():
    mysql.execute("select `id` from `workoo`.`eastmoney_list`")
    all_gubas = ["{:0>6}".format(x[0]) for x in mysql.fetchall()]

    with open('./data/lack.json', 'r', encoding='utf-8') as fn:
        new_gubas = json.loads(fn.read())

    for guba in all_gubas:
        if guba not in new_gubas:
            mysql.execute(
                "select * from `workoo`.`eastmoney_count` where `GubaId` = {} and `type` = '1'"
                .format(guba))
            data = [{
                'GubaId': guba,
                'Date': x[3],
                'Count': x[4]
            } for x in mysql.fetchall()]
            mongo['count'].insert_many(data)
            print('{} is down'.format(guba))


mongo = init_mongo()
mysql = init_mysql()

if __name__ == "__main__":
    DataClean().main()
    # clean_date()
    unify_data()