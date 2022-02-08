
proj_cate = {'研发类项目': 'RDD21120823567MO0', '交付类项目': 'RDD211208234PZ0XS', '市场类项目': 'RDD211208235G4JNK', '政府类项目': 'RDD211208235S84G0', '其他类项目': 'RDD2112082360UI9S', '运营类项目': 'RDD2112193H5QWLC', '测试类项>目': 'RDD2112193HT13EO'}

proj_budget = 
def mk_push_data():
    dd_url = "https://oapi.dingtalk.com/gettoken?appkey=dinglvvlvdoluezrxwkm&appsecret=Lm9CE6Ljna4K0TTKzDUSIPyKus5TjCCD9J8M25C4ASgPrSELnQoi-rUMfquVQnxL"    
    res = requests.get(dd_url)
    change_dict = json.loads(res.text)
    cache.set("access_token", change_dict['access_token'], 7200)
    return change_dict['access_token']
