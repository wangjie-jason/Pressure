# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/10/16 15:35
# @Author : wangjie
# @File : task_mq.py
# @project : Pressure

"""
初始化django_task_mq消息队列中间件（整个工程只运行1次即可）
import os
from django_task_mq import mq_init

mq_init(os.path.dirname(os.path.abspath(__file__)))
"""
# 新增消费者
import os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % 'Pressure')  # 引号中请输入您的setting父级目录名
django.setup()

from MyApp.models import DB_django_task_mq
from django_task_mq import mq_consumer
from MyApp.views import play_tasks

mq_consumer(DB_django_task_mq, play_tasks, topic='yace')
