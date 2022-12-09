# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/12/8 16:23
# @Author : wangjie
# @File : material_management.py.py
# @project : Pressure


import requests


def t():
    url = "https://lins-api.zibo.sensoro.vip:8443/device/v1/mobile/devices/domains"

    payload = {}
    headers = {
        'Host': 'lins-api.zibo.sensoro.vip:8443',
        'content-type': 'application/json; charset=utf-8',
        'x-client-appversion': '1.0.0',
        'x-client-idfa': 'E110FEEB-A5EC-4696-B284-F157EFC45D18',
        'accept': 'application/json,text/xml, application/xml, text/javascript, text/json, application/javascript, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8,*/*;q=0.5',
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNTk4MjI0NTIwODkxMDY0MzIxIiwiY2xpZW50SWQiOiJmOTBhOTNkZmU0YTQzZTRlOWIxZjQ0YTY4MjY4NGMwYSIsImFwcElkIjoicEp0aXFqQ0FTWUFLZGlGRm1wTm9SOSIsIm5pY2tuYW1lIjoi546L5pm25pm2IiwiZXhwIjoxNjcxMDk2ODUwLCJpYXQiOjE2NzA0OTIwNTAsInVzZXJuYW1lIjoiKzg2MTg2MDIxNTA2ODAiLCJyZWZyZXNoVG9rZW4iOiIxMjhkZGU5NzFkZWY0MmM3OTY4ZGJjMWVkY2QwMzI4NyIsIm1lcmNoYW50SWQiOiIwIiwidXNlcklkIjoiMTU5ODIyNDUyMDk4NzUzMzMxNCJ9.jQE5RQIKpYKWvNOOmybuTgKcJPtXrqw9acV5P21o8NwROB_wXu4YoZnBjJJFbTkUKJtXH4mVyK4AyI-5Gq9_Sg',
        'x-client-archivetype': 'release or debug',
        'x-lins-merchantid': '0',
        'accept-language': 'zh-CN',
        'x-client-devicetype': 'iPhone 8',
        'x-lins-view': 'all',
        'x-client-systemversion': '13.7',
        'language': 'zh-Hans-CN;q=1.0',
        'x-client-system': 'iOS',
        'x-client-channel': '2000',
        'user-agent': 'Lins/1.0.0 (iPhone 8 com.sensoro.linszibo; build:1; iOS 13.7.0) Alamofire/5.6.1',
        'encoding': 'gzip;q=1.0, compress;q=0.5'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    # print('domains接口请求完成')

    url = "https://lins-api.zibo.sensoro.vip:8443/statistics/v2/statistics/cameras/resources?endTime=1670515199000&startTime=1669910400000"

    payload = {}
    headers = {
        'Host': 'lins-api.zibo.sensoro.vip:8443',
        'x-client-appversion': '1.0.0',
        'content-type': 'application/json; charset=utf-8',
        'encoding': 'gzip;q=1.0, compress;q=0.5',
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNTk4MjI0NTIwODkxMDY0MzIxIiwiY2xpZW50SWQiOiJmOTBhOTNkZmU0YTQzZTRlOWIxZjQ0YTY4MjY4NGMwYSIsImFwcElkIjoicEp0aXFqQ0FTWUFLZGlGRm1wTm9SOSIsIm5pY2tuYW1lIjoi546L5pm25pm2IiwiZXhwIjoxNjcxMDk2ODUwLCJpYXQiOjE2NzA0OTIwNTAsInVzZXJuYW1lIjoiKzg2MTg2MDIxNTA2ODAiLCJyZWZyZXNoVG9rZW4iOiIxMjhkZGU5NzFkZWY0MmM3OTY4ZGJjMWVkY2QwMzI4NyIsIm1lcmNoYW50SWQiOiIwIiwidXNlcklkIjoiMTU5ODIyNDUyMDk4NzUzMzMxNCJ9.jQE5RQIKpYKWvNOOmybuTgKcJPtXrqw9acV5P21o8NwROB_wXu4YoZnBjJJFbTkUKJtXH4mVyK4AyI-5Gq9_Sg',
        'accept': 'application/json,text/xml, application/xml, text/javascript, text/json, application/javascript, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8,*/*;q=0.5',
        'x-lins-merchantid': '0',
        'x-client-archivetype': 'release or debug',
        'accept-language': 'zh-CN',
        'x-client-devicetype': 'iPhone 8',
        'x-lins-view': 'all',
        'x-client-systemversion': '13.7',
        'x-client-system': 'iOS',
        'language': 'zh-Hans-CN;q=1.0',
        'user-agent': 'Lins/1.0.0 (iPhone 8 com.sensoro.linszibo; build:1; iOS 13.7.0) Alamofire/5.6.1',
        'x-client-channel': '2000',
        'x-client-idfa': 'E110FEEB-A5EC-4696-B284-F157EFC45D18'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    # print('cameras_resources接口请求完成')

    url = "https://lins-api.zibo.sensoro.vip:8443/mobile/v1/mobile/devices/subsystems/"

    payload = {}
    headers = {
        'Host': 'lins-api.zibo.sensoro.vip:8443',
        'content-type': 'application/json; charset=utf-8',
        'x-client-appversion': '1.0.0',
        'encoding': 'gzip;q=1.0, compress;q=0.5',
        'accept': 'application/json,text/xml, application/xml, text/javascript, text/json, application/javascript, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8,*/*;q=0.5',
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNTk4MjI0NTIwODkxMDY0MzIxIiwiY2xpZW50SWQiOiJmOTBhOTNkZmU0YTQzZTRlOWIxZjQ0YTY4MjY4NGMwYSIsImFwcElkIjoicEp0aXFqQ0FTWUFLZGlGRm1wTm9SOSIsIm5pY2tuYW1lIjoi546L5pm25pm2IiwiZXhwIjoxNjcxMDk2ODUwLCJpYXQiOjE2NzA0OTIwNTAsInVzZXJuYW1lIjoiKzg2MTg2MDIxNTA2ODAiLCJyZWZyZXNoVG9rZW4iOiIxMjhkZGU5NzFkZWY0MmM3OTY4ZGJjMWVkY2QwMzI4NyIsIm1lcmNoYW50SWQiOiIwIiwidXNlcklkIjoiMTU5ODIyNDUyMDk4NzUzMzMxNCJ9.jQE5RQIKpYKWvNOOmybuTgKcJPtXrqw9acV5P21o8NwROB_wXu4YoZnBjJJFbTkUKJtXH4mVyK4AyI-5Gq9_Sg',
        'x-lins-merchantid': '0',
        'x-client-archivetype': 'release or debug',
        'accept-language': 'zh-CN',
        'x-client-devicetype': 'iPhone 8',
        'x-client-systemversion': '13.7',
        'x-lins-view': 'all',
        'language': 'zh-Hans-CN;q=1.0',
        'user-agent': 'Lins/1.0.0 (iPhone 8 com.sensoro.linszibo; build:1; iOS 13.7.0) Alamofire/5.6.1',
        'x-client-channel': '2000',
        'x-client-system': 'iOS',
        'x-client-idfa': 'E110FEEB-A5EC-4696-B284-F157EFC45D18'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    # print('devices_subsystems接口请求完成')


t()
