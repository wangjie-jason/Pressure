# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/11/6 16:00
# @Author : wangjie
# @File : o.py
# @project : Pressure
import time, random

res = random.randint(1, 10)
time.sleep(res)
if res % 2 == 0:
    raise Exception
print('我是other脚本', time.time())
