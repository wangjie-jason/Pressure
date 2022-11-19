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


def get_all_times(request):  # 线程数计划[10,10,10,10,10],all_times[step][{0:2,1:3,4:2},{},{}],已经启动的总线程数-已经结束的线程数
    task_id = request.GET['task_id']
    res = {}  # 最终返回的大字典
    # all_times从数据库拿到的整个任务所有阶段及轮的时间集合[[{0:2,1:3,4:2},{}],[{}]]
    all_times = eval(DB_Tasks.objects.filter(id=int(task_id))[0].all_times)
    # all_threads从数据库拿到的整个任务所有的线程数集合[[10,10,10,10,10],[],[]]
    all_threads = eval(DB_Tasks.objects.filter(id=int(task_id))[0].all_threads)
    print(all_times)
    print(all_threads)
    legend_data = []  # echarts的标题
    max_time = 0  # 每个阶段所用的最大时间，用来控制echarts的y轴的最大值
    series = []  # echarts的y轴的数据
    x_pass = 0  # 计算x轴起点的变量，区分每阶段的起始点
    time_detail = []  # 报告所需的时间详情[step_avg_time,step_50_time,step_80_time,step_90_time,step_95_time,step_99_time,]
    for step in range(len(all_times)):  # step是下标，该循环遍历所有的阶段
        ###########################   计算time_detail，也就是表格的数据
        step_detail = {}
        step_all_time = 0  # 阶段总消耗时间
        for d in all_times[step]:  # d是每一轮的时间字典{0:1,2:3,3:2}
            step_all_time += sum([key * d[key] for key in d])  # [0,6,6]->12->加等得出每一阶段的总时间
        step_detail['step_avg_time'] = '%.2f' % (step_all_time / sum(all_threads[step]))  # 每阶段平均时间=每阶段总时间/每阶段总线程数

        child = 0  # 设置一个不断成长的时间，当已完成线程到50%，80%，90%，95%，99%时，将child赋值给对应的step_xx_line
        all_threads_count = sum(all_threads[step])  # 阶段总线程数
        while True:
            over_thread_count = 0  # 阶段内已经结束的线程
            for d in all_times[step]:  # d是每一轮的时间字典{0:1,2:3,3:2}
                over_thread_count += sum(d[key] for key in d if key <= child)  # d[key]取出字典value就是线程数,<=child代表取的是完成的线程数
            step_list = [0.5, 0.8, 0.9, 0.95, 0.99]  # 线程完成成功率的列表，50% LINE，80% LINE，90% LINE，95% LINE，99% LINE
            for sl in step_list:
                if over_thread_count >= all_threads_count * sl:
                    try:  # 如果step_detail['step_xx_line']已存在，即已经赋值过，就不做任何操作
                        step_detail['step_%d_line' % int(sl * 100)]
                    except:  # 如果step_detail['step_xx_line']不存在，就将child赋值给它
                        step_detail['step_%d_line' % int(sl * 100)] = str(child) + 's'
                        if sl == step_list[-1]:
                            break  # 打破for循环,且不执行else里的内容
            else:  # for循环执行完时，执行else里的内容
                child += 1
                continue  # 跳过后面语句，直接进行下一次while循环，防止外层的break打破while循环
            break

        time_detail.append(step_detail)
        ###############################

        # -----------------------计算折线图数据
        legend_data.append('阶段【%s】平均时间' % str(step + 1))
        legend_data.append('阶段【%s】线程数' % str(step + 1))
        max_tmp = max([max(all_times[step][d]) + d for d in range(len(all_times[step]))])  # 每个阶段所用的最大时间
        max_time += max_tmp + 1  # +1是因为每轮直接相隔1s
        avg_time = [''] * x_pass  # 平均时间
        threads_ = [''] * x_pass  # 执行中的线程数
        x_pass += max_tmp + 1  # +1是因为每轮直接相隔1s

        all_begin_threads = 0  # 已经启动的线程数

        for j in range(max_tmp + 1):  # 该循环遍历阶段的每个自然秒，j代表已经经过的自然秒
            all_pass_time = 0  # 总消耗的时间
            all_over_thread = 0  # 总结束的线程数
            for d in range(len(all_times[step])):  # d代表该阶段内的轮数,all_times[step][d]是每一轮的数据{0:1,2:3,3:2}，j-d代表补偿每轮中间相隔的那1s
                all_pass_time += sum([key * all_times[step][d][key] for key in all_times[step][d] if key <= (j - d)])
                all_over_thread += sum([all_times[step][d][key] for key in all_times[step][d] if key <= (j - d)])
            try:  # 总结束的线程数不为0时执行
                avg_time.append(  # (100 if request.GET['bh_switch'] == 'true' else 1))：当bh_switch=true时，将平均时间*100倍
                    float('%.2f' % (all_pass_time / all_over_thread)) * (
                        100 if request.GET['bh_switch'] == 'true' else 1))  # 平均时间=总消耗的时间/总结束的线程数
            except:  # 0不能作为除数，所以当总结束的线程数为0时，直接赋值为空
                avg_time.append('')
            try:  # 按自然秒从阶段内取已经开始的线程数，all_threads[step]=[10,10,10]
                all_begin_threads += all_threads[step][j]
            except:  # 防止下标越界，当j的值超过阶段all_threads[step]的下标时，直接pass
                pass
            threads_.append(all_begin_threads - all_over_thread)  # 执行中的线程数=已经启动的线程数-总结束的线程数
            # print(all_begin_threads)
        # print(avg_time)
        series.append({'type': 'line', 'name': '阶段【%s】平均时间' % str(step + 1), 'data': avg_time})
        series.append({'type': 'line', 'name': '阶段【%s】线程数' % str(step + 1), 'data': threads_})

    option = {
        'legend_data': legend_data,
        'xAxis_data': list(range(max_time)),
        "series": series
    }
    # {'name': '项目3', "data": [6, 21, 12, 19, 22, 15, 9, 2, 32, 5, 12, 36], 'type': 'line'}
    res['option'] = option
    res['thread_detail'] = all_threads
    res['time_detail'] = time_detail
    return HttpResponse(json.dumps(res))
