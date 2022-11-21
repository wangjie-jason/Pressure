# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/10/21 18:18
# @Author : wangjie
# @File : test1.py
# @project : Pressure
import time
import random


def t(key):
    res = random.randint(1, 10)
    time.sleep(res)
    if res % 2 == 0:
        raise Exception
