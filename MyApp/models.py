from django.db import models


# Create your models here.
class DB_Projects(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, default='new project')
    plan = models.CharField(max_length=1000, null=True, blank=True, default='[]')  # 压测计划，专用的关键字语法。（可保存成模版）
    variable = models.CharField(max_length=1000, null=True, blank=True, default='[]')  # 变量设置[{'key':'a','value':1},{}]

    def __str__(self):
        return self.name


class DB_Tasks(models.Model):
    stime = models.CharField(max_length=30, null=True, blank=True, default='')
    des = models.CharField(max_length=300, null=True, blank=True, default='')
    project_id = models.IntegerField(default=0)
    status = models.CharField(max_length=10, null=True, blank=True, default='队列中')  # 队列中 ， 压测中，已结束。
    mq_id = models.IntegerField(default=0)
    stop = models.BooleanField(default=False)  # 终止状态
    all_times = models.CharField(max_length=5000, null=True, blank=True, default=[])  # 整个任务所有阶段及轮的时间
    all_threads = models.CharField(max_length=5000, null=True, blank=True, default=[])  # 整个任务所有的线程数
    all_fail_threads = models.CharField(max_length=5000, null=True, blank=True, default=[])  # 整个任务所有失败的线程数

    def __str__(self):
        return self.des


class DB_django_task_mq(models.Model):
    topic = models.CharField(max_length=100, null=True, blank=True, default="")
    message = models.TextField(default="{}")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.topic
