import re
import json
import time
import js2py
import datetime
from bson import ObjectId

from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup
from config import DEBUG, logger, mongo, get_cookie


def magic_time():
    second = mongo['cookie'].find_one(
        {'_id': ObjectId('5e03287f913800005e007d28')})['waiting']
    time.sleep(second)


def get_detail(path):
    global header_fyeds, header_snssdk

    if 'jinritemai' in path:
        info = {}
        info['id'] = path.split('=')[-1]
        info['link'] = path
        header_snssdk['Referer'] = path
        path = 'https://ec.snssdk.com/product/fxgajaxstaticitem?b_type_new=0&id={}'.format(
            info['id'])
        resp = req(path, header=header_snssdk)
        data = json.loads(resp)
        phone = data['data'].get('mobile')
        second_phone = data['data'].get('second_mobile')
        shop_phone = data['data'].get('shop_tel')
        phones = []
        if phone:
            phones.append(phone)
        if second_phone:
            phones.append(second_phone)
        if shop_phone:
            phones.append(shop_phone)

        info['shop_name'] = data['data'].get('shop_name')
        info['company_name'] = data['data'].get('company_name')
        info['phone'] = phone

        return info
    # elif 'fyeds' in path:
    #     header_fyeds['Host'] = path.split('/')[2]
    #     resp = req(path, header=header_fyeds)
    #     contact = soup(resp, attr={'id': 'contact_tel'})
    #     if contact:
    #         return [contact['href'].replace('tel:', '')]
    #     else:
    #         return []
    else:
        logger.error('the detail link is {}'.format(path))
        return


def get_path(uuid):
    resp = req(path=redirect_path.format(uuid), header=header)
    js_obj = re.search(js_pattern, resp)
    js_obj = js_obj.group().replace('window.location=', 'return ')
    js_function = js2py.eval_js(js_obj)
    path = js_function()
    resp = req(path=f'{host}/{path}', header=header)

    return resp


def fang_xing():
    for page in range(5000):
        path = 'https://bkbs.baokuanbushou.com/s.stp?action=dy_data_search&key=&cat=&cat2=&sort=5&size=10&page={page}&biz_type=4&create_begin=&stcallback=_jsonph5unux5hfz'
        resp = req(path, header=header)
        json_obj = re.search(json_pattern, resp)
        data = json.loads(json_obj.group(1))

        need_insert = []
        for item in data['items']:
            path = get_path(item['uuid'])
            info = get_detail(path)
            if info:
                need_insert.append(info)

        mongo["baokuanbushou"].insert_many(need_insert)


def lu_ban():
    path = 'https://bkbs.baokuanbushou.com/s.stp?action=dy_data_search&key=&cat=&cat2=&sort=8&size=10&page={page}&biz_type=1&create_begin=&stcallback=_jsonp9dp0b4rfklo'


def shops():
    path = 'https://bkbs.baokuanbushou.com/s.stp?action=dy_shop_search&key=&cat=&sort=8&size={page}0&page=1&stcallback=_jsonpr8db66koty'


def main():
    fang_xing()


req = Query().run
soup = DealSoup().judge
host = 'https://bkbs.baokuanbushou.com'
json_pattern = re.compile(r'^_json.*\(([\s\S]*)\)$')
js_pattern = re.compile(r'function doredirect\(\)([\s\S]*)\}')
redirect_path = 'https://bkbs.baokuanbushou.com/s.stp?action=dy_redirect_to_product&productid={}'
redirect2_path = 'https://bkbs.baokuanbushou.com/s.stp?action=dy_redirect_to_product2&productuid={}'

header = {
    'Host': 'bkbs.baokuanbushou.com',
    'Accept': '*/*',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'no-cors',
    # 'Referer':
    # 'https://bkbs.baokuanbushou.com/s.stp?action=dyhome_pc',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': get_cookie()
}
header_fyeds = {
    'Host': 'd9650aad.fyeds6.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
header_snssdk = {
    'Host': 'ec.snssdk.com',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://haohuo.jinritemai.com',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer':
    'https://haohuo.jinritemai.com/views/product/item?id=3375241637788821075',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

if __name__ == "__main__":
    main()