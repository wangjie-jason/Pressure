import json
import os
import time

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from MyApp.models import *

from django.shortcuts import render


# Create your views here.
def login_act(request):
    # 从前端获取用户信息数据
    form = json.loads(request.body)
    # 用这个用户名和密码去 用户数据库表中找，如果找到的是用户就ok，如果找到的是一个None 那就不ok。
    USER = auth.authenticate(username=form['username'], password=form['password'])
    if USER:  # 证明找到用户了
        auth.login(request, USER)
        request.session['username'] = form['username']
        return HttpResponse(json.dumps({"result": 0}))
    else:  # 证明用户名密码错误
        return HttpResponse(json.dumps({"result": 1}))


def register_act(request):
    # 从前端获取用户信息数据
    form = json.loads(request.body)
    # 用户名和密码去 直接注册，注册成功就ok，注册失败就说明用户名已存在
    try:
        user = User.objects.create_user(username=form['username'], password=form['password'])
        user.save()
        return HttpResponse(json.dumps({"result": 0}))
    except:
        return HttpResponse(json.dumps({"result": 1}))


def get_echarts_data(request):
    res = {
        'legend_data': ['项目1', '项目2', '项目3'],
        'xAxis_data': ['9-15', '9-16', '9-17', '9-18', '9-19', '9-20', '9-21', '9-22', '9-23', '9-24', '9-25', '9-26'],
        "series": [
            {'name': '项目1', "data": [3, 1, 2, 29, 32, 12, 52, 23, 51, 35, 26, 16], 'type': 'line'},
            {'name': '项目2', "data": [33, 12, 24, 2, 3, 2, 5, 13, 21, 25, 26, 26], 'type': 'line'},
            {'name': '项目3', "data": [6, 21, 12, 19, 22, 15, 9, 2, 32, 5, 12, 36], 'type': 'line'}
        ]
    }
    style = {
        'label': {
            'show': True,
            'position': 'bottom',
            'textStyle': {
                'fontSize': 10
            }
        },
        # 'smooth': True,
        # 'step': 'middle',
    }
    for i in range(len(res['series'])):
        res['series'][i].update(style)
    return HttpResponse(json.dumps(res), content_type='application/json')


def get_projects(request):
    projects = list(
        DB_Projects.objects.all().values())  # 会返回一个 列表内套字典  如 [{"name":"newproject","",""},{"name":"newproject2","",""}]
    return HttpResponse(json.dumps(projects), content_type='application/json')


def add_project(request):
    DB_Projects.objects.create()
    return get_projects(request)


def delete_project(request):
    project_id = request.GET['project_id']
    DB_Projects.objects.filter(id=project_id).delete()
    return get_projects(request)


def get_project_detail(request):
    project_id = request.GET['project_id']
    project_detail = list(DB_Projects.objects.filter(id=project_id).values())[0]
    project_detail['scripts'] = eval(project_detail['scripts'])
    return HttpResponse(json.dumps(project_detail), content_type='application/json')


def save_project(request):
    project_detail = json.loads(request.body.decode('utf-8'))
    project_id = project_detail['id']
    DB_Projects.objects.filter(id=project_id).update(**project_detail)
    return HttpResponse('')


def upload_script_file(request):
    my_file = request.FILES.get('script_file')
    file_name = str(my_file)
    with open('scripts/' + file_name, 'wb+') as fp:
        for i in my_file.chunks():
            fp.write(i)
    return HttpResponse('')


def get_script_list(request):
    script_list = os.listdir('scripts')
    return HttpResponse(json.dumps(script_list))


def get_tasks(request):
    tasks = list(DB_Tasks.objects.all().values())
    return HttpResponse(json.dumps(tasks))


def add_task(request):
    project_id = request.GET['project_id']
    des = request.GET['des']
    DB_Tasks.objects.create(des=des, project_id=int(project_id), stime=str(time.strftime('%Y-%m-%d %H:%M:%S')))
    return get_tasks(request)
