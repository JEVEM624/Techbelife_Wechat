# encoding:UTF-8
from flask import Flask, request, make_response, abort
import hashlib
from HBUT import *
from CharRobot import *
import xml.etree.ElementTree as ET
import time
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def Wechat():
    if request.method == 'GET':

        if len(request.args) < 4:
            abort(403)
        else:
            query = request.args
            echostr = query.get('echostr', '')
            if Auth(query):
                return make_response(echostr)
            else:
                abort(403)
    else:
        query = request.args
        if Auth(query):
            xml = ET.fromstring(request.data)
            ToUserName = xml.find("ToUserName").text
            FromUserName = xml.find("FromUserName").text
            MsgType = xml.find("MsgType").text

            if MsgType == 'event':
                Event = xml.find("Event").text
                if Event == 'subscribe':
                    return ReplyText(FromUserName, ToUserName, "感谢您的关注！｡:.ﾟヽ(*´∀`)ﾉﾟ.:")
                elif Event == 'unsubscribe':
                    DeleteUser(FromUserName)
                    return ReplyText(FromUserName, ToUserName, "")
            elif MsgType == 'text':
                Content = xml.find("Content").text
                return RecognizeText(Content,FromUserName,ToUserName)
            elif MsgType=='voice':
                Content =xml.find("Recongnition").text
                return RecognizeText(Content,FromUserName,ToUserName)
            else:
                return ReplyText(FromUserName, ToUserName, "我不明白你的意思")
        else:
            abort(403)


def ReplyText(ToUser, FromUser, Content):
    text = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    response = make_response(text % (ToUser, FromUser, str(int(time.time())), Content))
    response.content_type = 'application/xml'
    return response

def RecognizeText(Content,FromUserName,ToUserName):
    if (re.match(u'绑定', Content) != None):
        try:
            index = Content.find("+", 3)
            Username = Content[3:index]
            Password = Content[index + 1:]
            return ReplyText(FromUserName, ToUserName, AddUser(FromUserName, Username, Password))
        except:
            return ReplyText(FromUserName, ToUserName, "输入错误,请重新输入")
    elif (re.match(u'课表', Content) != None) and (len(Content) == 2):
        return ReplyText(FromUserName, ToUserName, GetSchedules(FromUserName))
    elif (re.match(u'查分', Content) != None) and (len(Content) == 2):
        return ReplyText(FromUserName, ToUserName, GetGrades(FromUserName))
    elif (re.match(u'解绑', Content) != None) and (len(Content) == 2):
        return ReplyText(FromUserName, ToUserName, DeleteUser(FromUserName))
    elif (re.match(u'历史成绩', Content) != None) and (len(Content) == 4):
        return ReplyText(FromUserName, ToUserName, GetHistoryGrades(FromUserName))
    else:
        return ReplyText(FromUserName, ToUserName, ChatWithTuling(Content, FromUserName))


def Auth(query):
    signature = query.get('signature', '')
    timestamp = query.get('timestamp', '')
    nonce = query.get('nonce', '')
    token = WechatToken
    s = [timestamp, nonce, token]
    s.sort()
    s = ''.join(s)
    if (hashlib.sha1(s).hexdigest() == signature):
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)