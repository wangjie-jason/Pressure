from django.db import models


# Create your models here.
class DB_Projects(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, default='new project')
    scripts = models.CharField(max_length=500, null=True, blank=True, default='')  # 关联的脚本名字，按顺序。
    plan = models.CharField(max_length=500, null=True, blank=True, default='')  # 压测计划，专用的关键字语法。（可保存成模版）

    def __str__(self):
        return self.name
