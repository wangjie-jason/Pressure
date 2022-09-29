import json
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse

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
