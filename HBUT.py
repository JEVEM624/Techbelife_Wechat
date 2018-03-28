# -*- coding: UTF-8 -*-
import random
import sqlite3
import json
import requests
from config  import *

import sys

reload(sys)
sys.setdefaultencoding('utf8')
#cache = Cache()
#cache = Cache(config={'CACHE_TYPE': 'simple'})
conn = sqlite3.connect('user.db')
cursor = conn.cursor()
#cursor.execute('create table user (OpenID Text primary key, Username Text,Password Text)')



def AddUser(openid,username,password):


    status=CheckUser(openid,username,password)
    if(status==0):
        cursor.execute("INSERT INTO user (OpenID,Username,Password) VALUES (?,?,?)",(openid, username, password))
        conn.commit()
        #cache.delete_memoized(openid)
        return "绑定成功"
    elif(status==1):
        return "帐号密码错误"
    elif(status==2):
        return "此帐号已绑定，请先解绑"

def CheckUser(openid,username,password):
    cursor.execute("SELECT * FROM user WHERE OPENID==?",[openid]);
    row = cursor.fetchone()
    if row != None:
        return 2

    else:
        urls = 'http://run.hbut.edu.cn/Account/LogOnForJson?Mobile=1&isRemember=0&UserName=' + username + '&Password=' + password + '&Role=Student'
        s = requests.session()
        r = s.get(urls)
        text = json.loads(r.text)
        code = text["Status"]
        return int(code)


def Login(openid):
    cursor.execute("SELECT * FROM user WHERE OPENID==?" , [openid])
    #print random.randrange(1, 100)
    row = cursor.fetchone()
    if row == None:
        return 1, '0', '0', '0'
    else:
        username = row[1]
        password = row[2]
        urls = 'http://run.hbut.edu.cn/Account/LogOnForJson?Mobile=1&isRemember=0&UserName=' + username + '&Password=' + password + '&Role=Student'
        s = requests.session()
        r = s.get(urls)
        text = json.loads(r.text)
        code = text["Status"]
        if code == 0:
            aspxauth = r.cookies[".ASPXAUTH"]
            role = r.cookies["Role"]
            userObjFullName = r.cookies["userObjFullName"]
            return code,aspxauth, userObjFullName,role
        elif code == 1:
            return code,'','',''


def GetGrades(openid):
    status,aspxauth,userObjFullName,role=Login(openid)
    if(status==1):
        return '查询失败，请重新绑定'
    else:

        s = requests.Session()
        s.cookies['.ASPXAUTH'] = aspxauth
        s.cookies['Role'] = role
        s.cookies['userObjFullName'] = userObjFullName
        # print s.cookies
        r = s.get("http://run.hbut.edu.cn/StuGrade/IndexRecentSemesterForJson")
        k = r.text
        k = k.replace("\\", "")
        k = k[1:-1]
        text = json.loads(k)
        result = text["Title"] + '\n' + '平均绩点:' + str(text["AverageGradePoint"]) + '\n'
        for i in text["StuGradeList"]:
            result = result + str(i["CourseName"]) + ":" + str(i["Grade"]) + '\n'

        return result

def GetHistoryGrades(openid):
    status,aspxauth,userObjFullName,role=Login(openid)
    if(status==1):
        return '查询失败，请重新绑定'
    else:
        #print random.randrange(100, 200)
        s = requests.Session()
        s.cookies['.ASPXAUTH'] = aspxauth
        s.cookies['Role'] = role
        s.cookies['userObjFullName'] = userObjFullName
        # print s.cookies
        r = s.get("http://run.hbut.edu.cn/StuGrade/IndexAllSemesterForJson")
        k = r.text
        k = k.replace("\\", "")
        k = k[1:-1]
        text = json.loads(k)
        result = text["Title"] + '\n' + '平均绩点:' + str(text["AverageGradePoint"]) + '\n'
        for i in text["StuGradeList"]:
            result = result + str(i["CourseName"]) + ":" + str(i["Grade"]) + '\n'

        return result

def DeleteUser(openid):
    cursor.execute("SELECT * FROM user WHERE OPENID==?" , [openid]);
    row=cursor.fetchone()
    if row==None:
        return '你的账号还没有绑定哟'
    else:
        cursor.execute("DELETE from user where OPENID==?", [openid]);
        conn.commit()
        #cache.delete_memoized('get_gread',openid)
        return '解绑成功'

def GetSchedules(openid):
    status, aspxauth, userObjFullName, role = Login(openid)
    if (status == 1):
        return '查询失败，请重新绑定'
    else:
        s = requests.Session()
        s.cookies['.ASPXAUTH'] = aspxauth
        s.cookies['Role'] = role
        s.cookies['userObjFullName'] = userObjFullName
        # print s.cookies
        r = s.get("http://run.hbut.edu.cn/ArrangeTask/MyselfScheduleForJson/")
        k = r.text
        k = k.replace("\\", "")
        k = k[1:-1]
        text = json.loads(k)
        result ="今天的课表如下:\n"
        for i in text["TimeScheduleList"]:
            result = result + str(i["CourseName"]) + ":" + str(i["Grade"]) + '\n'

        return result
