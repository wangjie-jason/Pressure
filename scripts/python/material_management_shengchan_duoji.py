# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/12/8 10:07
# @Author : wangjie
# @File : material_management_shengchan_duoji.py
# @project : Pressure

"""
物资管理列表的查询接口
"""
import requests


def t():
    url = "https://lins-api.sensoro.com/fire/v1/material/page?page=1"

    payload = {}
    headers = {
        'authority': 'lins-api.sensoro.com',
        'accept': '*/*',
        'accept-language': 'zh-CN',
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNTI1MDIxNDYxNDEwMTQ0MjU4Iiwibmlja25hbWUiOiLmsarmnbAiLCJleHAiOjE2NzExODYyNDEsImlhdCI6MTY3MDU4MTQ0MSwidXNlcm5hbWUiOiIrODYxMzcxODM5NTQ3OCIsInJlZnJlc2hUb2tlbiI6IjM4ZjhmN2UxZGY3NjQ3YjA4N2ZlMmY5ZmRlMzMzYjc0IiwibWVyY2hhbnRJZCI6IjEyODY1ODI2NDg0NzgxNDI0NjUiLCJ1c2VySWQiOiIxNTI1Mzg5MDExNDk5Mjc4MzM4In0.cXaSfBl7aP1K3fNaZcWuTMXgMbxNB0gHiBnh_NjJKWcuwDNXpxXeVWnuIXWyEq4IrTjk4uo_Ih2zgLjn3OYQWg',
        'origin': 'https://lins.sensoro.com',
        'referer': 'https://lins.sensoro.com/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-lins-merchantid': '1286582648478142465',
        'x-lins-view': 'all'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.status_code)
