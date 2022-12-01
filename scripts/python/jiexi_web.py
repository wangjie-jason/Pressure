# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/12/1 00:05
# @Author : wangjie
# @File : jiexi_web.py
# @project : Pressure
import time
from datetime import datetime
import re
import threading
import requests


def t(log_name):
    with open('../scripts/logs/' + log_name, 'r') as fp:  # 打开日志文件
        lines = fp.readlines()  # 获取日志文件所有的行，组成一个列表，每一行都是列表的一个元素
        for i in range(len(lines)):
            if lines[i]:  # 进行简单清洗，筛选出lins[i]不为空格或空行的内容
                # 算时间差
                if i != 0:  # 不是首条日志，就必须算两条之间的间隔时间，模拟用户真实的请求情况
                    # lins[i] = [30/Nov/2022 18:49:52] "GET /get_script_list/ HTTP/1.1" 200 74
                    s = re.findall(r'\[(.*?)\]', lines[i])[0]
                    time_now = time.mktime(datetime.strptime(s, "%d/%b/%Y %H:%M:%S").timetuple())  # 当前日志的时间
                    s = re.findall(r'\[(.*?)\]', lines[i - 1])[0]
                    time_previous = time.mktime(datetime.strptime(s, "%d/%b/%Y %H:%M:%S").timetuple())  # 上一条日志的时间
                    cha = time_now - time_previous  # 两条日志之间的间隔时间
                    time.sleep(cha)  # 等待间隔时间，模拟用户真实的请求间隔时间
                # 新建线程启动req
                r = threading.Thread(target=req, args=(lines[i],))
                r.daemon = True
                r.start()
                r.join()


def req(context):
    method = re.findall(r'"(.*?) ', context)[0]  # 解析请求方式
    host = '127.0.0.1:8000'  # 请求域名，根据流量回放的环境要求，自己填写
    agreement = context.split(' ')[4].split('/')[0].lower() + "://"  # 解析请求协议（http或https）
    path = context.split(' ')[3]  # 解析请求路由
    url = agreement + host + path  # 拼成完整的url
    headers = {  # 数据偏移，在headers中打上replay=y的标签，代表这些数据全是压测流量回放产生的数据，方便后续清理数据库
        'replay': 'y'
    }
    res = requests.request(method, url=url, headers=headers)
    print('-----------------', int(time.time()))
    print(res.text)
