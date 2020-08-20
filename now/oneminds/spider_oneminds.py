import os
import time
# import json

from configparser import ConfigParser
# import datetime
# from urllib.parse import urlparse, parse_qs, urlencode

from utils import logger, run_func, request

from utils.common import get_in
from utils.db import MysqlOpea
from utils.signer import magic


def remove(content: str):
    return content.replace('\r',
                           '').replace('\n',
                                       '').replace(' ',
                                                   '').replace('\xa0', '')


def get_timestamps():
    return int(time.time() * 1000)


def write(content):
    with open('./top_category.txt', 'a', encoding='utf-8') as fn:
        fn.write(content)
        fn.write('\n')


class MyParser(ConfigParser):
    def to_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        return d


class DealOneminds:
    def __init__(self, database={}):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            # Referer: https://servicewechat.com/wx975908a83811915b/49/page-frame.html
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.goods = []
        self.mysql = MysqlOpea(database)
        super().__init__()

    def goods_group(self):
        # uri = 'https://ec.oneminds.cn/api/goods/group?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&timestamp=1597390905005'
        uri = f'https://ec.oneminds.cn/api/goods/group?platform=2&session_id=&sid=100043&store_id={self.store_id}&timestamp={get_timestamps()}'
        resp = request(uri, header=self.header, json=True)
        if resp.get('code') != 200:
            return

        for top_category in resp.get('data'):
            self.big_name = top_category.get('name')
            self.big_id = top_category.get('id')

            if self.save_category:
                write(self.big_name)
                continue
            if self.big_name not in self.categories:
                continue

            self.top_catagory_id = self.mysql.insert_category(self.big_name)

            if not top_category.get('mid'):
                self.mid_name = self.big_name
                self.mid_id = 0
                self.sub_category_id = self.top_catagory_id
                self.goods_list()
                continue

            for sub_category in top_category.get('mid'):
                self.mid_name = sub_category.get('name')
                self.mid_id = sub_category.get('id')
                self.sub_category_id = self.mysql.insert_category(
                    self.mid_name, self.top_catagory_id)

                self.goods_list()

    def goods_list(self):
        count = 10
        page = 0
        while page * 10 <= count:
            uri = f'https://ec.oneminds.cn/api/goods/list?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&rp=10&page={page+1}&big_id={self.big_id}&mid_id={self.mid_id}&small_id=0&sort=&order=desc&qs=1&goods_type=0&keyword=&timestamp={get_timestamps()}'
            resp = request(uri, header=self.header, json=True)
            if not resp.get('data'):
                return

            count = resp.get('data').get('count')

            for data in resp.get('data').get('list'):
                self.good_id = data.get('id')
                self.goods_detail()

            page += 1

    @run_func()
    def goods_detail(self):
        uri = f'https://ec.oneminds.cn/api/goods?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&id={self.good_id}&goods_type=1&timestamp={get_timestamps()}'
        resp = request(uri, header=self.header, json=True)
        data = resp.get('data')
        good_info = {}
        common_info = {}
        good_info = {}

        if get_in(data, 'sku.activity_type') == 3:
            good_info['is_seckill'] = 1
        else:
            good_info['is_seckill'] = 0

        good_info['grounding'] = self.grounding

        good_info['goodsname'] = get_in(data, 'sku.goods_name')
        good_info['subtitle'] = get_in(data, 'base.sub_heads')
        good_info['productprice'] = get_in(data, 'sku.market_price')
        good_info['price'] = get_in(data, 'sku.sale_price')
        good_info['costprice'] = get_in(data, 'sku.price')
        good_info['sales'] = get_in(data, 'sku.market_price')
        good_info['codes'] = get_in(data, 'sku.sku_id')
        good_info['total'] = get_in(data, 'sku.store')

        good_id = self.mysql.insert_good(good_info)

        self.mysql.configure_category(self.sub_category_id, good_id)
        common_info['goods_id'] = good_id
        common_info['big_img'] = get_in(data, 'sku.pic')
        common_info['goods_start_count'] = get_in(data, 'base.min_buy_qty')
        common_info['video'] = get_in(data, 'base.video_list')
        # common_info['begin_time'] = ''
        # common_info['end_time'] = ''
        common_info['oneday_limit_count'] = get_in(data, 'sku.max_buy_qty')
        common_info['content'] = get_in(data, 'base.description')
        common_info['diy_arrive_details'] = self.diy_arrive_details
        common_info['pick_up_type'] = self.pick_up_type

        common_info[
            'video'] = common_info['video'][0] if common_info['video'] else ''
        self.mysql.insert_common(common_info)
        self.mysql.insert_image(good_id, get_in(data, 'pic_list'))

        logger.info(f'已添加 - {good_id}')

    def run(self, save_category=None, categories=[], fields={}, default={}):
        self.save_category = save_category
        self.categories = categories
        self.fields = fields
        self.session_id = '2400a8df7528c7c76e3190c5b17ac4c3'
        self.store_id = 6

        self.grounding = int(default.get('grounding'))
        self.diy_arrive_details = default.get('diy_arrive_details')
        self.pick_up_type = int(default.get('pick_up_type'))

        if self.grounding not in (0, 1):
            logger.error('输入正确的 grounding')
            return
        if not self.diy_arrive_details:
            self.diy_arrive_details = ''
        if self.pick_up_type not in (1, 2, 3, 4):
            logger.error('输入正确的 pick_up_type')
            return

        self.goods_group()


def main():
    config = MyParser()
    config.read('./config.ini', encoding='utf-8')
    config = config.to_dict()
    fields = config.get('Field')
    default = config.get('Default')
    database = config.get('DataBase')
    save_category = int(get_in(config, 'Category.save'))
    spider = DealOneminds(database)

    if save_category:
        os.remove('./top_category.txt')
        spider.run(save_category, fields=fields, default=default)
    else:
        with open('./top_category.txt', 'r', encoding='utf-8') as fn:
            categories = fn.read().split('\n')

        spider.run(categories=categories, fields=fields, default=default)


if __name__ == "__main__":
    magic()
    try:
        main()
    except Exception as exc:
        logger.error(f'运行失败 - {exc}')

    input('按任意键退出')
