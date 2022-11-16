# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2022/11/10 20:40
# @Author : wangjie
# @File : play.py
# @project : Pressure
import subprocess, threading, json, time, os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % 'Pressure')  # 引号中请输入您的setting父级目录名
django.setup()
from MyApp.models import DB_Tasks, DB_Projects, DB_django_task_mq


def play_tasks(mq):
    def doit_other(script_path, script_params, tmp):
        start_time = time.time()
        _bin = dz[script_name.split('.')[-1]]
        subprocess.call(_bin + ' ' + script_path + ' ' + script_params + ' mq_id=' + str(mq.id), shell=True)
        end_tims = time.time()
        cha = int(end_tims - start_time)  # 执行每个线程所耗费的时间，精确到秒

    def doit_python(script_path, script_params, tmp):
        start_time = time.time()
        exec('from scripts.python.%s import %s\n%s' % (
            script_name.split('.')[0], script_params.split('(')[0], script_params))
        end_tims = time.time()
        cha = int(end_tims - start_time)  # 执行每个线程所耗费的时间，精确到秒
        try:
            exec('round_times_%s[cha]+=1' % tmp)
        except:
            exec('round_times_%s[cha]=1' % tmp)

    def doit_go(script_path, script_params, tmp):
        print('go')

    def one_round(script_path, thread_num, script_model, script_params):
        # global round_times
        # round_times = {}  # 每轮所有线程的时间
        tmp = str(time.time()).replace('.', '')
        exec('global round_times_%s\nround_times_%s = {}' % (tmp, tmp))  # 每轮所有线程的时间
        ts = []
        target = {'other': doit_other, 'python': doit_python, 'go': doit_go}[script_model]
        for n in range(thread_num):
            t = threading.Thread(target=target, args=(script_path, script_params, tmp))
            t.daemon = True
            ts.append(t)
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        print('-------------结束了一轮压测--------------')
        step_times.append(eval('round_times_%s' % tmp))

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
    for step in plan:  # step=阶段
        step_times = []  # 每个阶段所包含的所有轮的时间
        script_model = step['name'].split('/')[0]
        script_name = step['name'].split('/')[1]
        script_params = step['script_params']
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', script_model,
                                   script_name)
        trs = []
        if '+' in step['old_num']:  # 无限增压
            task_rounds = 100
        elif '_' in step['old_num']:  # 瞬时增压
            task_rounds = int(step['old_round']) * (step['old_num'].count('_') + 1)
        else:
            task_rounds = int(step['old_round'])

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
            tr = threading.Thread(target=one_round, args=(script_path, thread_num, script_model, script_params))
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
    print('【整个压测任务结束】', all_times)
    task.update(status='已结束', all_times=all_times)


if __name__ == '__main__':
    mq_id = sys.argv[1].split('=')[1]
    mq = DB_django_task_mq.objects.filter(id=int(mq_id))[0]
    play_tasks(mq)
