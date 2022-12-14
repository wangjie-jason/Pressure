# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/11/10 20:40
# @Author : wangjie
# @File : play.py
# @project : Pressure
import re
import subprocess, threading, json, time, os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % 'Pressure')  # 引号中请输入您的setting父级目录名
django.setup()

from MyApp.models import DB_Tasks, DB_Projects, DB_django_task_mq
from random import randint  # read_sp解析随机数字用的，不要删
from faker import Faker  # mock数据的库，read_sp解析随机前端传过来的faker方法用的

fake = Faker(locale='zh_CN')  # 使mock的数据是中国的（姓名、身份证等。。。）


def str_time_s():
    return str(time.time())[:10]


def str_time_ms():
    return str(time.time())[:14]


def str_time_μs():
    return str(time.time())


def data_file(row, index):  # 每个线程内有几个变量就执行几次
    content = data_file_content_list[row].replace('\n', '').split(' ')[index]
    try:
        content = eval(content)
    except:
        pass
    return content


def read_sp(script_params, script_model):  # 将前端变量设置处的参数转换成script_params
    old = {}
    if use_file:  # 需要使用数据文件时，才求row，否则不求
        row = randint(0, len(data_file_content_list) - 1)  # data_file()内使用的，在data_file()前赋值，防止row在一个线程内多次随机

    for i in variable:
        old[i['key']] = eval(i['value'])  # {'a':1,'b':2}
    if script_model == 'other':
        p_list = []
        params = [i for i in script_params.split(' ') if i]
        for i in params:
            p_list.append('"' + repr(old[i]) + '"')
        end = ' '.join(p_list)
    elif script_model == 'python':
        p_list = []
        params = re.findall(r'\((.*?)\)', script_params)[0].split(',')  # ['a','b'] 或 ['100','200']
        if params != ['']:  # params不为空时，才走for循环的逻辑，防止不需要传参的压测脚本解析参数时报错
            for i in params:
                try:  # ['100','200']能求值走这里
                    eval(i)  # 100
                    p_list.append(repr(eval(i)))  # 100
                except:  # ['a','b']不能求值走这里
                    p_list.append(repr(old[i]))  # 得出old['a']:1,repr(old['a']:'1'
        # print('p_list:', p_list)  # p_list：['1','2']
        end = script_params.split('(')[0] + '(' + ','.join(p_list) + ')'  # ''.join拼接时会扒一层双引号或单引号，得出end='t(1,2)'
        # print('end：', end)

    return end


def play_tasks(mq):
    def doit_other(script_path, script_params, tmp):
        script_params = read_sp(script_params, script_model)
        start_time = time.time()
        _bin = dz[script_name.split('.')[-1]]
        s = subprocess.call(_bin + ' ' + script_path + ' ' + script_params + ' mq_id=' + str(mq.id), shell=True)
        if s != 0:  # subprocess.call的返回值等于0代表成功，否则代表失败
            exec('round_fail_threads_%s["fail"]+=1' % tmp)
        end_tims = time.time()
        cha = int(end_tims - start_time)  # 执行每个线程所耗费的时间，精确到秒
        try:
            exec('round_times_%s[%s]+=1' % (tmp, cha))  # 如果字典里有这个Key就直接+1
        except:
            exec('round_times_%s[%s]=1' % (tmp, cha))  # 如果字典里没有这个Key就直接等于1

    def doit_python(script_path, script_params, tmp):
        script_params = read_sp(script_params, script_model)
        start_time = time.time()
        try:
            exec('from scripts.python.%s import %s\n%s' % (
                script_name.split('.')[0], script_params.split('(')[0], script_params))
        except Exception as e:  # 异常代表线程执行失败，则将round_fail_threads_%s中的"fail"+1来统计失败数
            print("异常原因：", e)
            exec('round_fail_threads_%s["fail"]+=1' % tmp)
        end_tims = time.time()
        cha = int(end_tims - start_time)  # 执行每个线程所耗费的时间，精确到秒
        try:
            exec('round_times_%s[%s]+=1' % (tmp, cha))  # 如果字典里有这个Key就直接+1
        except:
            exec('round_times_%s[%s]=1' % (tmp, cha))  # 如果字典里没有这个Key就直接等于1

    def doit_go(script_path, script_params, tmp):
        print('go')

    def one_round(script_path, thread_num, script_model, script_params, pj):
        # global round_times
        # round_times = {}  # 每轮所有线程的时间
        tmp = str(time.time()).replace('.', '')
        exec('global round_times_%s\nround_times_%s = {}' % (tmp, tmp))  # 每轮所有线程的时间
        step_times.append(eval('round_times_%s' % tmp))

        exec('global round_fail_threads_%s\nround_fail_threads_%s = {"fail":0}' % (tmp, tmp))  # 每轮所有失败的线程数
        step_fail_threads.append(eval('round_fail_threads_%s' % tmp))

        ts = []
        target = {'other': doit_other, 'python': doit_python, 'go': doit_go}[script_model]

        if pj:  # 是否要平均发出请求
            if thread_num != 1:
                rest = 1 / (thread_num - 1)  # 设置一个休息时间，使压测方式为持续压测时，线程按1s内平均发出去，而不是瞬时全部发出
            else:
                rest = 0
        else:
            rest = 0

        for n in range(thread_num):
            t = threading.Thread(target=target, args=(script_path, script_params, tmp))
            t.daemon = True
            ts.append(t)
        for t in ts:
            t.start()
            time.sleep(rest)
        for t in ts:
            t.join()
        print('-------------结束了一轮压测--------------')

    dz = {'py': 'python3', 'java': 'java', 'php': 'php'}  # 后缀对应doit_other启动对应语言的脚本命令
    message = json.loads(mq.message)
    task_id = message['task_id']
    task = DB_Tasks.objects.filter(id=int(task_id))
    task.update(status='压测中')
    # -----
    # 根据这个任务关联的项目id，去数据库找出这个项目的所有内容。
    project = DB_Projects.objects.filter(id=int(task[0].project_id))[0]
    plan = eval(project.plan)
    all_times = []  # 整个任务所有阶段及轮的时间
    all_threads = []  # 整个任务所有的线程数
    all_fail_threads = []  # 整个任务所有失败的线程数

    # 是否需要使用数据文件
    global variable
    variable = eval(project.variable)  # 也在read_sp()内使用，数据格式为[{'key':'a','value':'1'},{'key':b,'value':'2'},{}]
    global use_file
    use_file = False  # 判断是否需要使用数据文件的开关
    for v in variable:
        if v['value'][:9] == 'data_file':
            use_file = True

    if use_file:  # 如果需要使用数据文件
        # 拿出前端变量设置里传的文件数据 ##########
        file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data_files',
                                 'data_file_' + str(project.id))
        if os.path.exists(file_name):  # 项目已上传文件，即file_name存在
            with open(file_name) as fp:
                global data_file_content_list
                data_file_content_list = fp.readlines()
                if len(data_file_content_list) == 0:  # 如果文件内容为空
                    task.update(status='异常[文件内容为空]', all_times=all_times, all_threads=all_threads,
                                all_fail_threads=all_fail_threads)
                    raise Exception('任务终止！文件内容为空')
        else:  # 如果项目未上传文件，即file_name不存在
            task.update(status='异常[文件不存在]', all_times=all_times, all_threads=all_threads,
                        all_fail_threads=all_fail_threads)
            raise Exception('任务终止！文件不存在')

    #######################
    all_steps = len(plan)  # 整个压测计划的阶段数
    over_steps = 0  # 已经结束的阶段数，初始值为0

    for step in plan:  # step=阶段
        step_times = []  # 每个阶段所包含的所有轮的时间
        step_threads = []  # 每个阶段所包含的线程数
        step_fail_threads = []  # 每个阶段失败的线程数
        script_model = step['name'].split('/')[0]
        script_name = step['name'].split('/')[1]
        script_params = step['script_params']
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', script_model,
                                   script_name)
        trs = []
        pj = False  # 判断是否需要平均发出请求的开关
        if 's' in step['old_round']:  # 当为持续压测时，即old_round = xxxs时，就平均发出请求
            pj = True
        step['old_round'] = step['old_round'].split('s')[0]  # 虚假需求，支持持续压测时，去掉old_round传的s。old_round=120s
        if '+' in step['old_num']:  # 无限增压
            task_rounds = 100
        elif '_' in step['old_num']:  # 瞬时增压
            task_rounds = int(step['old_round']) * (step['old_num'].count('_') + 1)
        else:
            task_rounds = int(step['old_round'])
        #############################
        for r in range(task_rounds):  # round = 5  r = 0,1,2,3,4
            if '/' in step['old_num']:  # 阶梯增压 0-10/90-5
                mid = step['old_num']  # 10/90
                thread_num = int(int(mid.split('/')[0]) + (int(mid.split('/')[1]) - int(mid.split('/')[0])) / (
                        task_rounds - 1) * r)
            elif '+' in step['old_num']:  # 无限增压 0-10+5
                mid = step['old_num']  # 10+
                thread_num = int(int(mid.split('+')[0]) + int(step['old_round']) * r)
            elif '_' in step['old_num']:  # 瞬时增压 0-10_100_1000-5   r=0,1,2,3,4=10=0   r=5,6,7,8,9=100=1
                mid = step['old_num'].split('_')  # [10,100,1000]
                thread_num = int(mid[int(r / int(step['old_round']))])
            else:
                thread_num = int(step['old_num'])
            #############################

            step_threads.append(thread_num)
            tr = threading.Thread(target=one_round, args=(script_path, thread_num, script_model, script_params, pj))
            tr.daemon = True
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
        print('-------------结束了一个阶段--------------')
        all_times.append(step_times)
        all_threads.append(step_threads)
        all_fail_threads.append(step_fail_threads)
        over_steps += 1  # 每结束一个阶段，整个压测计划的结束阶段就+1
        task.update(progress=float(over_steps / all_steps) * 100)  # 进度=结束阶段数/总阶段数，*100是前端展示时直接展示具体的数字加%
    print('【整个压测任务结束】')
    # print('all_times:', all_times)
    # print('all_fail_threads:', all_fail_threads)
    task.update(status='已结束', all_times=all_times, all_threads=all_threads, all_fail_threads=all_fail_threads)


if __name__ == '__main__':
    mq_id = sys.argv[1].split('=')[1]
    mq = DB_django_task_mq.objects.filter(id=int(mq_id))[0]
    play_tasks(mq)
