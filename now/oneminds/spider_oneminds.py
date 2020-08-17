# import os
# import json
import time
# import datetime
# from urllib.parse import urlparse, parse_qs, urlencode

from utils import logger, run_func, request, excel, soup, mongo


def remove(content: str):
    return content.replace('\r',
                           '').replace('\n',
                                       '').replace(' ',
                                                   '').replace('\xa0', '')


def get_timestamps():
    return int(time.time() * 1000)


class DealOneminds:
    def __init__(self):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            # Referer: https://servicewechat.com/wx975908a83811915b/49/page-frame.html
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.goods = []
        super().__init__()

    def goods_group(self):
        # uri = 'https://ec.oneminds.cn/api/goods/group?platform=2&session_id=12a1fb58723ae572f4354510d05db8d2&sid=100043&store_id=58&timestamp=1597390905005'
        uri = f'https://ec.oneminds.cn/api/goods/group?platform=2&session_id=&sid=100043&store_id=58&timestamp={get_timestamps()}'
        resp = request(uri, header=self.header, json=True)
        if resp.get('code') != 200:
            return

        for top_category in resp.get('data'):
            self.big_id = top_category.get('id')
            self.big_name = top_category.get('name')

            for sub_category in top_category.get('mid'):
                self.mid_id = sub_category.get('id')
                self.mid_name = sub_category.get('name')

                self.goods_list()

    def goods_list(self):
        uri = f'https://ec.oneminds.cn/api/goods/list?platform=2&session_id=12a1fb58723ae572f4354510d05db8d2&sid=100043&store_id=58&rp=10&page={page}&big_id=114&mid_id=0&small_id=0&sort=&order=desc&qs=1&goods_type=0&keyword=&timestamp={get_timestamps()}'
        count = 10
        page = 1
        while page * 10 > count:
            resp = request(uri, header=self.header, json=True)
            count = resp.get('data').get('count')

            for data in resp.get('data').get('list'):
                self.good_id = data.get('id')
                self.goods_detail()

    def goods_detail(self):
        uri = f'https://ec.oneminds.cn/api/goods?platform=2&session_id=12a1fb58723ae572f4354510d05db8d2&sid=100043&store_id=58&id={self.good_id}&goods_type=1&timestamp={get_timestamps()}'
        resp = request(uri, header=self.header, json=True)

    def run(self):
        pass


def main():
    print(resp)


def spider():
    main()

    # try:
    #     name = excel.save()
    # except Exception as exc:
    #     logger.error(f'保存失败 - {exc}')
    # else:
    #     logger.info(f'保存成功 - {name}')

    # input('按任意键退出')


if __name__ == "__main__":
    # magic()
    spider()