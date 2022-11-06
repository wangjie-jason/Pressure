import json
import os
import re
import subprocess
import sys
import threading
import time

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django_task_mq import mq_producer

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
    script_model = request.POST.get('script_model')
    my_file = request.FILES.get('script_file')
    file_name = str(my_file)
    with open('scripts/' + script_model + '/' + file_name, 'wb+') as fp:
        for i in my_file.chunks():
            fp.write(i)
    return HttpResponse('')


def get_script_list(request):
    script_list = []
    for d in ('other', 'python', 'go'):
        script_list += [d + '/' + i for i in os.listdir(os.path.join('scripts', d))]
    return HttpResponse(json.dumps(script_list))


def get_tasks(request):
    tasks = list(DB_Tasks.objects.all().values())[::-1]
    return HttpResponse(json.dumps(tasks))


def add_task(request):
    project_id = request.GET['project_id']
    des = request.GET['des']
    new_task = DB_Tasks.objects.create(des=des, project_id=int(project_id),
                                       stime=str(time.strftime('%Y-%m-%d %H:%M:%S')))
    mq_id = mq_producer(DB_django_task_mq, topic='yace', message={'task_id': new_task.id})
    new_task.mq_id = mq_id
    new_task.save()
    return get_tasks(request)


def play_tasks(mq):
    def doit_other(script_path):
        print('other')
        subprocess.call('python3 ' + script_path + ' mq_id=' + str(mq.id), shell=True)

    def doit_python(script_path):
        print('python')

    def doit_go(script_path):
        print('go')

    def one_round(script_path, thread_num, script_model):
        ts = []
        target = {'other': doit_other, 'python': doit_python, 'go': doit_go}[script_model]
        for n in range(thread_num):
            t = threading.Thread(target=target, args=(script_path,))
            t.setDaemon(True)
            ts.append(t)
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        print('-------------结束了一轮压测--------------')

    message = json.loads(mq.message)
    task_id = message['task_id']
    task = DB_Tasks.objects.filter(id=int(task_id))
    task.update(status='压测中')
    # -----
    # 根据这个任务关联的项目id，去数据库找出这个项目的所有内容。
    project = DB_Projects.objects.filter(id=int(task[0].project_id))[0]
    scripts = eval(project.scripts)
    for step in project.plan.split(','):  # step=阶段
        script = scripts[int(step.split('-')[0])].split('/')
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', script[0],
                                   script[1])
        trs = []
        if '+' in step:  # 无限增压
            task_rounds = 100
        elif '_' in step:  # 瞬时增压
            task_rounds = int(step.split('-')[2]) * (step.count('_') + 1)
        else:
            task_rounds = int(step.split('-')[2])

        for r in range(task_rounds):  # round = 5  r = 0,1,2,3,4
            if '/' in step:  # 阶梯增压 0-10/90-5
                mid = step.split('-')[1]  # 10/90
                thread_num = int(int(mid.split('/')[0]) + (int(mid.split('/')[1]) - int(mid.split('/')[0])) / (
                        task_rounds - 1) * r)
            elif '+' in step:  # 无限增压 0-10+5
                mid = step.split('-')[1]  # 10+5
                thread_num = int(int(mid.split('+')[0]) + int(mid.split('+')[1]) * r)
            elif '_' in step:  # 瞬时增压 0-10_100_1000-5   r=0,1,2,3,4=10=0   r=5,6,7,8,9=100=1  r=10,11,12,13,14=1000=2
                mid = step.split('-')[1].split('_')  # [10,100,1000]
                thread_num = int(mid[int(r / int(step.split('-')[2]))])
            else:
                thread_num = int(step.split('-')[1])
            tr = threading.Thread(target=one_round, args=(script_path, thread_num,script[0]))
            tr.setDaemon(True)
            trs.append(tr)
        for tr in trs:  # tr=轮
            # 路障
            now_task = DB_Tasks.objects.filter(id=task_id)[0]
            if now_task.stop:
                break
            tr.start()
            time.sleep(1)
        for tr in trs:
            tr.join()
        print('-------------结束了一个阶段的压测计划--------------')
    print('【整个压测任务结束】')
    task.update(status='已结束')


def stop_task(request):
    def stop_mac():
        ts = subprocess.check_output('ps -ef | grep mq_id=%s | grep -v "grep"' % str(mq_id), shell=True)
        for t in str(ts).split('mq_id=' + str(mq_id)):
            s = re.findall(r'\b(\d+?)\b', t)[:3]
            if s:
                pid = max([int(i) for i in s])
                subprocess.call('kill -9 ' + str(pid), shell=True)

    def stop_windows():
        ts = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)
        for t in str(ts).split(r'\n'):
            if 'mqid=' + str(mq_id) in t:
                pid = re.findall(r'\b(\d+?)\b', t)[-1]
                subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)

    task_id = request.GET['id']
    task = DB_Tasks.objects.filter(id=int(task_id))[0]
    mq_id = task.mq_id
    if task.status == '队列中':
        DB_django_task_mq.objects.filter(id=int(mq_id)).delete()
        task.status = '队列中时结束'
        task.stop = True
        task.save()
    elif task.status == '压测中':
        task.stop = True
        task.save()
        for j in range(100):
            now_task = DB_Tasks.objects.filter(id=int(task_id))[0]
            if now_task.status == '压测中':
                try:
                    if sys.platform in ('win32', 'win64'):
                        stop_windows()
                    else:
                        stop_mac()
                except:
                    break
                finally:
                    now_task.status = '压测中时结束'
                    now_task.save()
            else:
                break
    else:
        return HttpResponse(json.dumps({"errorCode": 300, "data": [], "Message": "任务已结束"}))
    return HttpResponse(json.dumps({"errorCode": 200, "data": [], "Message": "终止成功"}))
