import json
import requests
import datetime
import re
import HBUT

class Schedule:
    def __init__(self,username,password):
        self.url = 'http://run.hbut.edu.cn/ArrangeTask/MyselfScheduleForJson'
        self.login_url = 'http://run.hbut.edu.cn/Account/LogOnForJson?Mobile=1&isRemember=0&UserName=' + username + '&Password=' + password + '&Role=Student'
        self.StartDay = (2018,3,5)

    def login(self):
        session = requests.Session()
        session.get(self.login_url)
        r = session.get(self.url)
        r.encoding='utf-8'
        dic={}
        if r.status_code == 200:
            json_text = r.text
            json_text = json_text.replace("\\","")
            json_text = json_text[1:-1]
            dic = json.loads(json_text)
        self.class_list = dic["TimeScheduleList"]

    def getClass(self,day,week):
        self.login()
        dayList = []
        classList = []

        for i in range(len(self.class_list)):
            if self.class_list[i]["Day"] == day:
                dayList.append(self.class_list[i])

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

    def getSchedule(self):
        now = (datetime.date.today()-datetime.date(self.StartDay[0],self.StartDay[1],self.StartDay[2])).days
        now_week = now/7+1
        now_day = now%7+1
        Classes = self.getClass(now_day,now_week)
        return Classes