import json
import os
import re
import subprocess
import sys
import time

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
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
    project_detail['plan'] = eval(project_detail['plan'])
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
    # script_list = []
    # for d in ['other', 'python', 'go']:
    #     script_list += [d + '/' + i for i in os.listdir(os.path.join('scripts', d))]
    script_list = [d + '/' + i for d in ['other', 'go', 'python'] for i in os.listdir(os.path.join('scripts', d))]
    # script_list = sum([[d + '/' + i for i in os.listdir(os.path.join('scripts', d))] for d in ['other', 'go', 'python']], [])
    # script_list = list(chain.from_iterable( numpy.array( [ [d+'/'+i  for i in os.listdir(os.path.join('scripts',d))]   for d in ['other','go','python']  ])))
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


def stop_task(request):
    def stop_mac():
        subprocess.call("kill -9 `ps -ef | grep mq_id=%s | grep -v 'grep' | awk '{print $2}'`" % str(mq_id), shell=True)
        # ts = subprocess.check_output('ps -ef | grep mq_id=%s | grep -v "grep"' % str(mq_id), shell=True)
        # for t in str(ts).split('mq_id=' + str(mq_id)):
        #     s = re.findall(r'\b(\d+?)\b', t)[:3]
        #     if s:
        #         pid = max([int(i) for i in s])
        #         subprocess.call('kill -9 ' + str(pid), shell=True)

    def stop_windows():
        ts = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)
        for t in str(ts).split(r'\n'):
            if 'mq_id=' + str(mq_id) in t:
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
        if sys.platform in ('win32', 'win64'):
            stop_windows()
        else:
            stop_mac()
        task.stop = True
        task.status = '压测中时结束'
        task.save()

    else:
        return HttpResponse(json.dumps({"errorCode": 300, "data": [], "Message": "任务已结束"}))
    return HttpResponse(json.dumps({"errorCode": 200, "data": [], "Message": "终止成功"}))


def clear_all(request):
    DB_Tasks.objects.all().delete()
    DB_django_task_mq.objects.all().delete()
    return HttpResponseRedirect('/')


def get_all_times(request):
    task_id = request.GET['task_id']
    res = {}
    all_times = eval(DB_Tasks.objects.filter(id=int(task_id))[0].all_times)
    print(all_times)
    legend_data = []
    max_time = 0
    series = []
    x_pass = 0  # 计算x轴起点

    for step in range(len(all_times)):
        legend_data.append('阶段【%s】平均时间' % str(step + 1))
        max_tmp = max([max(all_times[step][d]) + d for d in range(len(all_times[step]))])  # 每个阶段所用的最大时间
        max_time += max_tmp + 1
        avg_time = [''] * x_pass  # 平均时间
        x_pass += max_tmp + 1

        for j in range(max_tmp + 1):  # 循环每个阶段所用的总时长
            all_pass_time = 0  # 总消耗的时间
            all_over_thread = 0  # 总结束的线程数
            for d in range(len(all_times[step])):
                all_pass_time += sum([key * all_times[step][d][key] for key in all_times[step][d] if key <= (j - d)])
                all_over_thread += sum([all_times[step][d][key] for key in all_times[step][d] if key <= (j - d)])
            try:
                avg_time.append(float('%.2f' % (all_pass_time / all_over_thread)))
            except:
                avg_time.append('')
        print(avg_time)
        series.append({'type': 'line', 'name': '阶段【%s】平均时间' % str(step + 1), 'data': avg_time})

    option = {
        'legend_data': legend_data,
        'xAxis_data': list(range(max_time)),
        "series": series
    }
    # {'name': '项目3', "data": [6, 21, 12, 19, 22, 15, 9, 2, 32, 5, 12, 36], 'type': 'line'}
    res['option'] = option
    return HttpResponse(json.dumps(res))
