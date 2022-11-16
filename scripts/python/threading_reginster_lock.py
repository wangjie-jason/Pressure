# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/11/11 12:50
# @Author : wangjie
# @File : threading_reginster_lock.py
# @project : Pressure
import random, requests, json
import threading


def threading_reginster():
    name = []
    for i in range(1, 201):
        name.append('张' + str(i))
    name = random.choices(name)

    code = ''
    for i in range(4):
        a = random.randrange(10)
        code += str(a)
    IdCard = '42118119960513' + code

    url = "https://lins-test1-wx.sensoro.com/clientapp/v1/clientapp/register/apply/save"

    payload = json.dumps({
        "projectId": "1583360563481055234",
        "realName": f"{name[0]}",
        "idCard": f"{IdCard}",
        "userPicture": "https://s3.dianjun.sensoro.vip/lins-oss-prod/lsv1/clientuser/45033972379081032167356_400.jpg",
        "source": 1,
        "featureId": 1590633949693128700,
        "featureValue": "t1v8Z6wTrBStKQ3W3smHT7fJqoX8+2G2eBXs+tdQd0WxhcvXqk3AE4afP4Bib4CZVJXiHbjD70tCH02HHLjYozLnzdhZc/s44qvtRdjpuYoq4uUv5g/hrdnrqhxLA2UVW4WlrdfVGMyKtwBUpRA7zh5jmDt5jIwqR+1WWtxoktw7fI4dqXL14iDghk6564iaxEMVK65/VwvWfsBlE6EUEb7JnrbRgj73XRhcTYxo4C3nhWE+9RgbYxxZdkcZeLe8ZJadKNtZAiS/r75LOdpXj6aiN1dUikQUm3iMkkcwC4pCP1aMy/UlJl0d5WGsgjOikZjPyXg1aNzd+PAqlpsMLg==",
        "houseAddress": "点军区",
        "plateText": ""
    })
    headers = {
        'Host': 'lins-test1-wx.sensoro.com',
        'content-type': 'application/json',
        'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJjbGllbnRVc2VySWQiOiIxNTkxMDI0MTY1MzI0NjY4OTMwIiwiY2xpZW50QWNjb3VudElkIjoiMTU5MTAyNDE2NTM0NTY0MDQ1MCIsImNsaWVudEFwcElkIjoiMSIsImV4cCI6MTY2ODc3MDM3NiwiaWF0IjoxNjY4MTY1NTc2LCJyZWZyZXNoVG9rZW4iOiI5NmZhYmYxMjEyODY0YmY0OWE5YjQ3MGRiNDg0NDdjNCJ9.VENiLDweTPyFkQTnVfugbkX68-ayYiSdtH7kJV7ve4nZEEs6s0s0YX5HKBHWdFDGBPPHH4ZZIN8HGmOyBoHEHw',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d36) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxf16743037fe8e53b/7/page-frame.html'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json())


tr = []
for n in range(200):
    t = threading.Thread(target=threading_reginster)
    t.daemon = True
    tr.append(t)

error = 0
for t in tr:
    try:
        t.start()
    except:
        error += 1

for t in tr:
    t.join()
