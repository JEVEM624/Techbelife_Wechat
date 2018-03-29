import json
import requests
import datetime
from config import *
import re

url = 'http://run.hbut.edu.cn/ArrangeTask/MyselfScheduleForJson'

session = requests.Session()
username = ''
password = ''
login_url = 'http://run.hbut.edu.cn/Account/LogOnForJson?Mobile=1&isRemember=0&UserName=' + username + '&Password=' + password + '&Role=Student'

session.get(login_url)
r = session.get(url)
r.encoding='utf-8'
dic={}
if r.status_code == 200:
    json_text = r.text
    json_text = json_text.replace("\\","")
    json_text = json_text[1:-1]
    dic = json.loads(json_text)

class_list = dic["TimeScheduleList"]

def getClass(day,week):
    dayList = []
    classList = []

    for i in range(len(class_list)):
        if class_list[i]["Day"] == day:
            dayList.append(class_list[i])

    for Class in dayList:
        timeString = Class["Week"]
        times = re.findall("\d+\-\d+|\d+",timeString)
        for time in times:
            if time.find('-')!=-1:
                begin,end = time.split('-')
                begin = int(begin)
                end = int(end)
                if week <= end and week >= begin:
                    classList.append(Class)
            else:
                if week == int(time):
                    classList.append(Class)
    classList.sort(key = lambda a: a['DayTime'])
    return classList

now = (datetime.date.today()-datetime.date(StartDay[0],StartDay[1],StartDay[2])).days
now_week = now/7+1
now_day = now%7+1

Classes = getClass(now_day,now_week)
for Class in Classes:
    print(Class['CurName'])
    print(Class['Place'])
    print(Class['Teacher'])
    print(Class['DayTime'])
    print()
