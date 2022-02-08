import json

from django.shortcuts import render
from django.http import HttpResponse
from mkapi import models,tools
from datetime import datetime
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from . models import ProjectDD

res = {
        "status": "",
        "date": datetime.now(),
        "msg": ""
}

# Create your views here.
@csrf_exempt
def hello(request):
    body = eval(request.body)
    
    pmanager = body['pmanager'][0]
    puser = body['puser'][0]

    pmanager_name = tools.dd_get_username(pmanager)
    pmanager_num = tools.dd_get_usernumber(pmanager)
    puser_name = tools.dd_get_username(puser)
    
    proj = ProjectDD(puser=puser_name, pname=body['pname'], pnum=body['pnum'], pcate=body['pcate'], plevel=body['plevel'], pmanager=pmanager_name, ppay=body['ppay'])
    proj.save()

    tools.mk_proj_list(body['pname'], body['pnum'], body['pcate'], pmanager_num)
    tools.mk_proj_budget(body['pname'], body['pnum'], body['pcate'])
    tools.mk_proj_budget_plan(body['pnum'], body['ppay'])
    return HttpResponse("Hello world ! ")

@csrf_exempt
def test_post(request):
    body = eval(request.body)
    res['status'] = "success"
    print(body['pmanager'])
    
    puser_name = tools.dd_get_username(15125357561285996)
    print(puser_name)

    return HttpResponse("Hello world ! ")
