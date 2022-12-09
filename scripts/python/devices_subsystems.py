# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/12/8 16:25
# @Author : wangjie
# @File : devices_subsystems.py
# @project : Pressure

import requests

def t():
  url = "https://lins-test1-api.sensoro.com/mobile/v1/mobile/devices/subsystems/"

  payload = {}
  headers = {
    'Host': 'lins-test1-api.sensoro.com',
    'x-client-appversion': '1.20.6',
    'content-type': 'application/json; charset=utf-8',
    'encoding': 'gzip;q=1.0, compress;q=0.5',
    'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJhY2NvdW50SWQiOiIxNDc3NTQyMDEwNTk2NDc4OTc4IiwiY2xpZW50SWQiOiI4MThiYmM5NDdiNmM4OTkwMGQ4ZGMyODUxMmEzYmQwOCIsImFwcElkIjoiQnVKYXlFTmpZdkE4Sk1CcHdpbk1XMiIsIm5pY2tuYW1lIjoi5rGq5p2wIiwiZXhwIjoxNjcxMDY5OTA5LCJpYXQiOjE2NzA0NjUxMDksInVzZXJuYW1lIjoiKzg2MTM3MTgzOTU0NzgiLCJyZWZyZXNoVG9rZW4iOiIyNzk2NWY3ZTY2YmQ0NDBlYWM5YTExMDU1OGU0NGUwZCIsIm1lcmNoYW50SWQiOiIxMDAwMDAwMDEiLCJ1c2VySWQiOiIxNDc4MjExMDc1NTE3NTM4MzA2In0.cO4TRHqgtvNosinro4qZx06FrhLyVByANWwm6_bfhgKILHXLEyCYb-q9XZl-Oy0ra0zn7LsxJOv8iRXZueNMzg',
    'accept': 'text/xml, application/xml, application/json, text/javascript, text/json, application/javascript, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8,*/*;q=0.5',
    'x-lins-merchantid': '100000001',
    'x-client-archivetype': 'release or debug',
    'accept-language': 'zh-CN',
    'x-client-systemversion': '13.7',
    'x-lins-view': 'default',
    'x-client-devicetype': 'iPhone 8',
    'x-client-system': 'iOS',
    'user-agent': 'Lins/1.20.6 (iPhone 8 com.sensoro.SensoroLins; build:2; iOS 13.7.0) Alamofire/5.5.0',
    'x-client-channel': '2000',
    'language': 'zh-Hans-CN;q=1.0',
    'x-client-idfa': 'E110FEEB-A5EC-4696-B284-F157EFC45D18'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  print(response.text)
