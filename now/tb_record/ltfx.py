# coding:utf-8

import os
import datetime
import time
import chardet

import re
# import pandas as pd
import csv


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = (path.strip()).decode('utf-8')
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


# 检查是否包含关键字
def jiance(id, text):
    global kfid
    try:

        khtime = re.findall('\((.*?)\)', text, re.S)
        # print khtime
        kftime = re.findall('%s\((.*?)\)' % kfid.decode('gbk').encode('utf-8'),
                            text, re.S)
        # print kftime
        flag = 1
        for i in kftime:
            if i != khtime[0]:
                a = datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
                b = datetime.datetime.strptime(khtime[0], '%Y-%m-%d %H:%M:%S')
                if '0:00:01' == str(a - b):
                    # print a,b
                    continue

                data['回复时间（秒）'].append(str(a - b))
                # print i,khtime[0],a-b
                flag = 0
                break
        if flag:
            data['回复时间（秒）'].append('null')
    except:

        data['回复时间（秒）'].append('null')

    list = open('行业分类.txt'.decode('utf-8').encode('gbk')).read().split('\n')
    sss = '否'
    for i in list:
        if i.decode('gbk').encode('utf-8') in text:
            sss = i.decode('gbk').encode('utf-8')
            break
    data['是否包含关键字（行业）'].append(sss)

    list = open('包含关键字列表.txt'.decode('utf-8').encode('gbk')).read().split('\n')
    for i in list:
        if i.decode('gbk').encode('utf-8') in text:
            data['是否包含关键字（%s）' % i.decode('gbk').encode('utf-8')].append('是')
        else:
            data['是否包含关键字（%s）' % i.decode('gbk').encode('utf-8')].append('否')
    ltlist = text.split('\n')
    data['聊天记录'].append(text)
    flag = 1
    for lt in ltlist:
        if id in lt:

            try:
                phone = re.findall(':.*?(1[35678]\d{9})', lt)[0]
                data['手机号'].append(phone)
                # print(lt)
                data['手机号所在记录'].append(text)
                flag = 0
                break
            except:
                continue
    if flag:
        data['手机号'].append('null')
        data['手机号所在记录'].append('null')


# 读取分割每个客户的聊天记录
def duqu(path):
    global kfid
    global data
    f = open(path)
    kfid = f.readline().replace('\n', '')
    try:
        tt = guolv(f.read())
        text = ''

        text = re.findall(
            '================================================================.*?================================================================(.*?)================================================================',
            tt, re.S)[0]

        print('-', end=' ')
    except:
        text = re.findall(
            '================================================================.*?================================================================(.*?)================================================================',
            f.read(), re.S)[0]
        print('-', end=' ')
    #
    #
    # except:
    #     tt=f.read()
    #
    #     text = re.findall( '================================================================.*?================================================================(.*?)================================================================',tt, re.S)[0]

    list = text.split('----------------------------')
    for i in range(1, len(list), 2):

        try:

            jiance(list[i].decode('gbk').encode('utf-8'),
                   list[i + 1].decode('gbk').encode('utf-8'))
        except:

            continue
        data['客服ID'].append(kfid.decode('gbk').encode('utf-8'))

        data['客户ID'].append(list[i].decode('gbk').encode('utf-8'))
        # print list[i].decode('gbk').encode('utf-8')


    # for i in list:
    #     print i.decode('gbk').encode('utf-8')
    #     print('-----------')
def guolv(texts):
    text = texts
    for i in texts.split('\n'):
        # print(i)

        for line in open('过滤关键字列表.txt'.decode('utf-8').encode('gbk'),
                         'r').readlines():
            # print(line.decode('utf-8').encode('gbk'))
            if '\n' == line:
                continue
            if line.strip('\n').decode('utf-8-sig').encode('gbk') in i:
                # print(i.decode('gbk').encode('utf-8'))
                # print (i)
                text = text.replace(i, '')
    # print(text)
    return text


def main():
    rootdir = './O'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        try:
            path = os.path.join(rootdir, list[i])
            # print path
            duqu(path)
            print(path, end=' ')
            print('--分析成功！！')
        except:
            print('x')
            print(path, end=' ')
            print('==============分析失败！！')
            print('x')


if __name__ == '__main__':
    print('-淘宝聊天记录分析系统1.6 2019-5-22-')
    print('-欢迎使用，该程序以学习为目的，请勿传播或用于违法用途！ 技术支持 BY：无敌 QQ:2161396998')

    print('=====================')
    print('读取文件地址：', end=' ')
    mkdir('O')
    print('导出文件地址：', end=' ')
    mkdir('S')
    print('=====================')
    print('正在分析————')

    data = {
        '客服ID': [],
        '客户ID': [],
        '回复时间（秒）': [],
        '是否包含关键字（行业）': [],
        '手机号': [],
        '手机号所在记录': [],
        '聊天记录': []
    }
    cols = [
        '客服ID'.decode('utf-8').encode('gbk'),
        '客户ID'.decode('utf-8').encode('gbk'),
        '回复时间（秒）'.decode('utf-8').encode('gbk'),
        '是否包含关键字（行业）'.decode('utf-8').encode('gbk')
    ]
    list = open('包含关键字列表.txt'.decode('utf-8').encode('gbk'),
                'r').read().split('\n')
    for i in list:
        cols.append('是否包含关键字（%s）'.decode('utf-8').encode('gbk') % i)
        data.update({'是否包含关键字（%s）' % i.decode('gbk').encode('utf-8'): []})
    cols.append('手机号'.decode('utf-8').encode('gbk'))
    cols.append('手机号所在记录'.decode('utf-8').encode('gbk'))
    cols.append('聊天记录'.decode('utf-8').encode('gbk'))
    main()
    datetime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    with open('./S/%s.csv' % datetime, "wb+") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        csvwriter.writerow(cols)
    for x in range(len(data['客服ID'])):
        list = []
        for y in cols:
            list.append(data[y.decode('gbk').encode('utf-8')][x].decode(
                'utf-8').encode('gbk', 'ignore'))
            # print data[y.decode('gbk').encode('utf-8')][x].decode('utf-8').encode('gbk', 'ignore')
        with open('./S/%s.csv' % datetime, "ab+") as datacsv:
            # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
            csvwriter = csv.writer(datacsv, dialect=("excel"))
            # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
            csvwriter.writerow(list)

    # print data
    # df = pd.DataFrame(data)
    #
    # df = df.ix[:, cols]
    # datetime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    # df.to_csv('./S/%s.csv'%datetime, encoding="utf_8_sig")
    print('=====================')
    print('分析成功，文件以保存在：', end=' ')
    print('./S/%s.csv' % datetime)

    c = eval(input('====================='))


