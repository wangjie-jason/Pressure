# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/11/11 12:50
# @Author : wangjie
# @File : threading_reginster_lock.py
# @project : Pressure
import random, requests, json
import threading


def threading_reginster(sn):
    url = "https://lins-test1-wx.sensoro.com/enter/v1/anon/enter/distribute/logs"

    payload = {
        'sn': '06520017C7516B05'
    }

    response = requests.request("POST", url, json=payload)

    print(response.json())


# tr = []
# for n in range(100):
#     t = threading.Thread(target=threading_reginster)
#     t.daemon = True
#     tr.append(t)
#
# error = 0
# success = 0
# for t in tr:
#     try:
#         t.start()
#         success += 1
#     except:
#         error += 1
# print('error:', error)
# print('success:', success)
#
# for t in tr:
#     t.join()
