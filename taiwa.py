#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 対談 Docomo vs Recruit
# http://qiita.com/alien/items/27e3289fb3b9a80f96c1

from time import sleep
import requests
import json
import types

D_KEY = ''
R_KEY = ''

# 1回目の呼び出し（会話の開始）
endpoint_r = 'https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk'
endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=REGISTER_KEY'
url = endpoint.replace('REGISTER_KEY', D_KEY)
url_r = endpoint_r
response_r = []

for i in range(15):
    if(i == 0):
        payload_d = {'utt' : 'はじめ'}
    else:
        payload_d = {'utt' : response_r[0]['reply']}

    #print(payload_d)

    headers_d = {'Content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload_d), headers=headers_d)
    data = r.json()

    response = data['utt']
    context = data['context']
    #print(data)
    print ("Do: %s" %(response))

    # 2回目の呼び出し
    payload_r = 'apikey='+R_KEY+'&query='+data['yomi']
    headers_r = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    #print (payload_r)

    r = requests.post(url_r, payload_r.encode('utf-8'), headers=headers_r)
    data = r.json()

    response_r = data['results']
    print ("Re: %s" %(response_r[0]['reply']))
sleep(1)
