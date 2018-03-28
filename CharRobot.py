#!/usr/bin/python
#coding:utf-8
import requests
import json
from config import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def ChatWithTuling(Content,Openid):

    inputText = {'text': Content}
    userInfo = {'apiKey': TulingApiKey, 'userId': Openid}
    perception = {'inputText': inputText}
    data = {'perception': perception, 'userInfo': userInfo}
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    response = requests.post(url=url, data=json.dumps(data))
    response.encoding = 'utf-8'
    result = response.json()
    answer = result['results'][0]['values']['text']
    return answer