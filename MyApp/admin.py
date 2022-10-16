from django.contrib import admin

# Register your models here.
from MyApp.models import *

admin.site.register(DB_Projects)
admin.site.register(DB_Tasks)
admin.site.register(DB_django_task_mq)
