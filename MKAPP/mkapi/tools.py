import os,requests
import http.client
import json
import time
import hashlib
import urllib.request
import urllib.parse
import urllib
import requests
from django.core.cache import cache

proj_cate = {'项目清单': 'RD2111111V80K70G', '研发类项目': 'RDC2112011WUF99MO', '交付类项目': 'RDC2112011WUML7R4', '市场类项目': 'RDC2112011WUSVXMO', '政府类项目': 'RDC2112011WV55IWW', '其他类项目': 'RDC2112011WVM36YO', '运营类项目': 'RDC2112011X9WSRY8', '测试类项目': 'RDC211215Z4LQ6F4'}

proj_level = {'项目等级': 'RD2111191HX0RI0W', 'A': 'RDD2111191HXM7W1S', 'B': 'RDD2111191HXST24G', 'C': 'RDD2111191HXST24G'}

proj_budget = {'研发类项目': 'BDG21121511WUS0OW', '交付类项目': 'BDG21121511TGDBPC', '市场类项目': 'BDG21121511S84328', '政府类项目': 'BDG21121511TV7PMO', '其他类项目': 'BDG21121511U4LXFK', '运营类项目': 'BDG21121511TOFVCW', '测试类项目': 'BDG21121511MSTFNK'}

proj_budget_plan = {'测试项目预算方案': 'BDG211116193228ZK'}

def mk_get_tokenid():
    appSecret = "B35ACAD6D8A406AE9FF82936939D8EAF"
    appCode = "AP2YZ7FBKOUF4X"
    timestamps = round(time.time() * 1000)
    var1 = appSecret + ":" + appCode + ":" + str(timestamps)
    sha256 = hashlib.sha256()
    sha256.update(var1.encode())
    secret = sha256.hexdigest()
    params = json.dumps({"secret": secret,"appCode": appCode,"timestamp": timestamps})
    headers = {"Content-type": "application/json"}
    conn = http.client.HTTPSConnection("dt.maycur.com")
    conn.request('POST', '/api/openapi/auth/login', params, headers)
    response = conn.getresponse()
    #code = response.status
    #reason=response.reason
    data = json.loads(response.read().decode('utf-8'))
    cache.set("entCode", data['data']['entCode'], 1800)
    cache.set("tokenId", data['data']['tokenId'], 1800)
    conn.close()

def dd_get_accesstoken():
    dd_url = "https://oapi.dingtalk.com/gettoken?appkey=dinglvvlvdoluezrxwkm&appsecret=Lm9CE6Ljna4K0TTKzDUSIPyKus5TjCCD9J8M25C4ASgPrSELnQoi-rUMfquVQnxL"    
    res = requests.get(dd_url)
    change_dict = json.loads(res.text)
    cache.set("access_token", change_dict['access_token'], 7200)
    return change_dict['access_token']

def dd_get_usernumber(userid):
    accesstoken = cache.get("access_token")
    if accesstoken is None:
        accesstoken = dd_get_accesstoken()
        accesstoken = cache.get("access_token")    
    dd_api = 'https://oapi.dingtalk.com/user/get?access_token=' + accesstoken + '&userid=' + str(userid)
    res = requests.get(dd_api)
    change_dict = json.loads(res.text)
    return change_dict['jobnumber']

def dd_get_username(userid):
    accesstoken = cache.get("access_token")
    if accesstoken is None:
        accesstoken = dd_get_accesstoken()
        accesstoken = cache.get("access_token")    
    dd_api = 'https://oapi.dingtalk.com/user/get?access_token=' + accesstoken + '&userid=' + str(userid)
    res = requests.get(dd_api)
    change_dict = json.loads(res.text)
    return change_dict['name']

def mk_proj_list(pname, pnum, pcate, puser_num):
    tokenid = cache.get("tokenId")
    entcode = cache.get("entCode")
    if tokenid is None:
        tokenid = mk_get_tokenid()
        tokenid = cache.get("tokenId")
        entcode = cache.get("entCode")
    
    headers = {"Content-type": "application/json", "entCode":entcode, "tokenId":tokenid}
    body = '{\"bizCode\":\"' + proj_cate['项目清单'] + '\",\"referenceDataDetails\":[{\"name\":\"' + pname + '\",\"bizCode\":\"' + pnum + '\",\"categoryBizCode\":\"' + proj_cate[pcate] + '\",\"principals\":[\"' + puser_num +'\"],\"enabled\":true}]}'
    params = body.encode("utf-8")

    conn = http.client.HTTPSConnection("dt.maycur.com")
    conn.request('POST', '/api/openapi/reference/data/detail', params, headers)
    response = conn.getresponse()
    res = json.loads(response.read().decode('utf-8'))
    conn.close()

def mk_proj_budget(pname, pnum, pcate):
    tokenid = cache.get("tokenId")
    entcode = cache.get("entCode")
    if tokenid is None:
        tokenid = mk_get_tokenid()
        tokenid = cache.get("tokenId")
        entcode = cache.get("entCode")

    headers = {"Content-type": "application/json", "entCode": entcode, "tokenId": tokenid}
    body = '{\"budgetOrgBizCode\":\"' + pnum + '\",\"budgetOrgCategoryBizCode\":\"' + proj_budget[pcate] + '\",\"budgetOrgName\":\"' + pname + '\",\"priority\":1,\"conditions\":[[{\"targetType\":\"REFERENCE_DATA_DETAIL\",\"targetObject\":{\"bizCode\":\"' + proj_cate['项目清单'] + '\",\"itemBizCode\":[\"' + pnum + '\"]}}]]}'
    url = 'https://dt.maycur.com/api/openapi/budget/org/save'
    params = body.encode("utf-8")
    res = requests.put(url, data=params, headers=headers)

def mk_proj_budget_plan(pnum, ppay):
    tokenid = cache.get("tokenId")
    entcode = cache.get("entCode")
    if tokenid is None:
        tokenid = mk_get_tokenid()
        tokenid = cache.get("tokenId")
        entcode = cache.get("entCode")

    headers = {"Content-type": "application/json", "entCode": entcode, "tokenId": tokenid}
    body = '{\"budgetPlanBizCode\":\"' + proj_budget_plan['测试项目预算方案'] + '\",\"budgets\":[{\"budgetOrgBizCode\":\"' + pnum + '\",\"budgetUnits\":[{\"periodNum\":1,\"budgetAmount\":' + ppay + '}]}]}'
 
    url = 'https://dt.maycur.com/api/openapi/budget/unit/batch'
    params = body.encode("utf-8")
    res = requests.put(url, data=params, headers=headers)
