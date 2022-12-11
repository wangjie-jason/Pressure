# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/12/8 16:23
# @Author : wangjie
# @File : devices_domains.py
# @project : Pressure


import requests


def t():
    # --------------------------------------------------
    url = "https://lins-api.sensoro.com/device/v1/mobile/devices/domains"

    payload = {}
    headers = {
        'Host': 'lins-api.sensoro.com',
        'content-type': 'application/json; charset=utf-8',
        'x-client-appversion': '1.20.6',
        'encoding': 'gzip;q=1.0, compress;q=0.5',
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNTI1MDIxNDYxNDEwMTQ0MjU4IiwiY2xpZW50SWQiOiI4MThiYmM5NDdiNmM4OTkwMGQ4ZGMyODUxMmEzYmQwOCIsImFwcElkIjoiQnVKYXlFTmpZdkE4Sk1CcHdpbk1XMiIsIm5pY2tuYW1lIjoi5rGq5p2wIiwiZXhwIjoxNjcxMTg0NjM5LCJpYXQiOjE2NzA1Nzk4MzksInVzZXJuYW1lIjoiKzg2MTM3MTgzOTU0NzgiLCJyZWZyZXNoVG9rZW4iOiJkYzQwMjg5YmJkNTM0Zjc2OTk5ZDBiYmM1Yzg2MWU2NCIsIm1lcmNoYW50SWQiOiIxMjg2NTgyNjQ4NDc4MTQyNDY1IiwidXNlcklkIjoiMTUyNTM4OTAxMTQ5OTI3ODMzOCJ9.4xvACQEggX4uHZ3wEMtYkskPGqysMlNtTAvUechiFIp6Z7NzinuAhpwEWVLmbupvBgXV9ppXvjdYpz2Pre3WsQ',
        'accept': 'text/xml, application/xml, application/json, text/javascript, text/json, application/javascript, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8,*/*;q=0.5',
        'x-lins-merchantid': '1286582648478142465',
        'x-client-archivetype': 'release or debug',
        'accept-language': 'zh-CN',
        'x-client-systemversion': '13.7',
        'x-client-devicetype': 'iPhone 8',
        'x-lins-view': 'all',
        'x-client-system': 'iOS',
        'user-agent': 'Lins/1.20.6 (iPhone 8 com.sensoro.SensoroLins; build:2; iOS 13.7.0) Alamofire/5.5.0',
        'x-client-channel': '2000',
        'language': 'zh-Hans-CN;q=1.0',
        'x-client-idfa': 'E110FEEB-A5EC-4696-B284-F157EFC45D18'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print('domains接口请求完成', response.status_code)

    # --------------------------------------------------
    url = "https://lins-api.sensoro.com/statistics/v2/statistics/cameras/resources?endTime=1670601599000&startTime=1669996800000"

    payload = {}
    headers = {
        'Host': 'lins-api.sensoro.com',
        'x-client-appversion': '1.20.6',
        'content-type': 'application/json; charset=utf-8',
        'encoding': 'gzip;q=1.0, compress;q=0.5',
        'accept': 'text/xml, application/xml, application/json, text/javascript, text/json, application/javascript, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8,*/*;q=0.5',
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNTI1MDIxNDYxNDEwMTQ0MjU4IiwiY2xpZW50SWQiOiI4MThiYmM5NDdiNmM4OTkwMGQ4ZGMyODUxMmEzYmQwOCIsImFwcElkIjoiQnVKYXlFTmpZdkE4Sk1CcHdpbk1XMiIsIm5pY2tuYW1lIjoi5rGq5p2wIiwiZXhwIjoxNjcxMTg0NjM5LCJpYXQiOjE2NzA1Nzk4MzksInVzZXJuYW1lIjoiKzg2MTM3MTgzOTU0NzgiLCJyZWZyZXNoVG9rZW4iOiJkYzQwMjg5YmJkNTM0Zjc2OTk5ZDBiYmM1Yzg2MWU2NCIsIm1lcmNoYW50SWQiOiIxMjg2NTgyNjQ4NDc4MTQyNDY1IiwidXNlcklkIjoiMTUyNTM4OTAxMTQ5OTI3ODMzOCJ9.4xvACQEggX4uHZ3wEMtYkskPGqysMlNtTAvUechiFIp6Z7NzinuAhpwEWVLmbupvBgXV9ppXvjdYpz2Pre3WsQ',
        'x-lins-merchantid': '1286582648478142465',
        'x-client-archivetype': 'release or debug',
        'accept-language': 'zh-CN',
        'x-client-systemversion': '13.7',
        'x-client-devicetype': 'iPhone 8',
        'x-lins-view': 'all',
        'x-client-system': 'iOS',
        'language': 'zh-Hans-CN;q=1.0',
        'user-agent': 'Lins/1.20.6 (iPhone 8 com.sensoro.SensoroLins; build:2; iOS 13.7.0) Alamofire/5.5.0',
        'x-client-channel': '2000',
        'x-client-idfa': 'E110FEEB-A5EC-4696-B284-F157EFC45D18'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print('cameras_resources接口请求完成', response.status_code)

    # --------------------------------------------------
    url = "https://lins-api.sensoro.com/mobile/v1/mobile/devices/subsystems/"

    payload = {}
    headers = {
        'Host': 'lins-api.sensoro.com',
        'x-client-appversion': '1.20.6',
        'content-type': 'application/json; charset=utf-8',
        'x-client-idfa': 'E110FEEB-A5EC-4696-B284-F157EFC45D18',
        'accept': 'text/xml, application/xml, application/json, text/javascript, text/json, application/javascript, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8,*/*;q=0.5',
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNTI1MDIxNDYxNDEwMTQ0MjU4IiwiY2xpZW50SWQiOiI4MThiYmM5NDdiNmM4OTkwMGQ4ZGMyODUxMmEzYmQwOCIsImFwcElkIjoiQnVKYXlFTmpZdkE4Sk1CcHdpbk1XMiIsIm5pY2tuYW1lIjoi5rGq5p2wIiwiZXhwIjoxNjcxMTg0NjM5LCJpYXQiOjE2NzA1Nzk4MzksInVzZXJuYW1lIjoiKzg2MTM3MTgzOTU0NzgiLCJyZWZyZXNoVG9rZW4iOiJkYzQwMjg5YmJkNTM0Zjc2OTk5ZDBiYmM1Yzg2MWU2NCIsIm1lcmNoYW50SWQiOiIxMjg2NTgyNjQ4NDc4MTQyNDY1IiwidXNlcklkIjoiMTUyNTM4OTAxMTQ5OTI3ODMzOCJ9.4xvACQEggX4uHZ3wEMtYkskPGqysMlNtTAvUechiFIp6Z7NzinuAhpwEWVLmbupvBgXV9ppXvjdYpz2Pre3WsQ',
        'x-lins-merchantid': '1286582648478142465',
        'x-client-archivetype': 'release or debug',
        'accept-language': 'zh-CN',
        'x-client-systemversion': '13.7',
        'x-lins-view': 'all',
        'x-client-devicetype': 'iPhone 8',
        'language': 'zh-Hans-CN;q=1.0',
        'user-agent': 'Lins/1.20.6 (iPhone 8 com.sensoro.SensoroLins; build:2; iOS 13.7.0) Alamofire/5.5.0',
        'x-client-channel': '2000',
        'x-client-system': 'iOS',
        'encoding': 'gzip;q=1.0, compress;q=0.5'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print('devices_subsystems接口请求完成', response.status_code)
