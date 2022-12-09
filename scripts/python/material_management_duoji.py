# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/12/8 10:07
# @Author : wangjie
# @File : material_management.py
# @project : Pressure

"""
物资管理列表的查询接口
"""
import requests


def t():
    url = "https://lins-api.zibo.sensoro.vip:8443/fire/v1/material/page"

    payload = {}
    headers = {
        'authority': 'lins-api.zibo.sensoro.vip:8443',
        'accept': '*/*',
        'accept-language': 'zh-CN',
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNTk4MjI0NTIwODkxMDY0MzIxIiwibmlja25hbWUiOiLnjovmmbbmmbYiLCJleHAiOjE2NzA4MjQ0NjcsImlhdCI6MTY3MDIxOTY2NywidXNlcm5hbWUiOiIrODYxODYwMjE1MDY4MCIsInJlZnJlc2hUb2tlbiI6ImE3NjgzNWNkY2NhMTRjYmJhYTU4ZTk2NWZlZmM1NTE0IiwibWVyY2hhbnRJZCI6IjAiLCJ1c2VySWQiOiIxNTk4MjI0NTIwOTg3NTMzMzE0In0.MWeHHQJO8Xs9f1CB2ZhiRzzI5-8LZ90ikqnfFoWK839SG_4FiJoi-Mj1zhA0VJCcCch-LHCwiTZa23DT6vP2Og',
        'origin': 'https://lins.zibo.sensoro.vip:8443',
        'referer': 'https://lins.zibo.sensoro.vip:8443/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-lins-merchantid': '0',
        'x-lins-view': 'all'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.status_code)

    # print(response.text)

