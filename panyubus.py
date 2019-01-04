#!/usr/bin/python
# -*- coding: UTF-8 -*-

import configparser
import requests
import random
import itchat
import json
import time
import ast
import os

from requests_toolbelt import MultipartEncoder

def get_img():
    image = {}
    url = "https://sm.ms/api/upload"
    headers = {
        'content-type': "multipart/form-data;",
        'cache-control': "no-cache",
    }
    multipart_encoder = MultipartEncoder(
        fields = {
            'smfile': ('QR.png', open('./QR.png', 'rb'), 'image/png')
        },
        boundary = '-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    headers['Content-Type'] = multipart_encoder.content_type
    response = requests.post(url, data=multipart_encoder, headers=headers)
    json_response = response.content.decode()
    dict_json = json.loads(json_response)
    if response.status_code != 200:
        print("图片上传失败")
    else:
        if dict_json.get("code") != "success" :
            print("图片上传失败")
        else:
            image["img_url"] = dict_json.get("data").get("url")
            image["del_url"] = dict_json.get("data").get("delete")
    return {"img_url" : image.get("img_url"), "del_url": image.get("del_url")}

def getDirection(bus):
    l = bus.get("l")
    startStation = l[0].get("n")
    endStation = l[len(l)-1].get("n")
    return startStation + "至" + endStation

def send_msg_to_user():
    # 这些是以后扩展时外部传进数据
    url = u"http://h5.thecampus.cc/api/v1/line?line_number=3150&direction=0"
    my_station = "石岗东村站"
    before_num = 3 #提前几站时告诉我

    Results = {}
    flag = 0
    try:
        dict = json.loads(requests.get(url).content.decode('utf-8'))
        # dict=ast.literal_eval(requests.get(url).content.decode('utf-8'))
    except Exception as e:
        print("实时公交数据获取失败！ Error: ")
        print(e)

    if dict.get("code") == 200 and dict.get("msg") == "ok":
        bus = dict.get("data").get("bus")
        Results["line"] = bus.get("rn")
        Results["direction"] = getDirection(bus)
        stations = bus.get("l")
        for station in stations:
            if station.get("n") == my_station:
                flag = stations.index(station)
        bus_status = stations[flag-before_num].get("bus_comming")
        if len(bus_status.get("bl")) == 0 and len(bus_status.get("bbl")) == 0:
            Results["status"] = 0
            Results["msg"] = "还未达到，请耐心等候..."
        else: 
            Results["status"] = 1
            Results["msg"] = "已到达" + stations[flag-before_num].get("n") + "，距您仅有 " + str(before_num) + " 站，请做好上车准备！"
    return Results

def qrCallback(uuid, status, qrcode):
    print("status: "+status)
    if status == '0':
        global qrSource
        qrSource = qrcode
        itchat.get_QR(uuid)
        send_QR()
    elif status == '200':
        qrSource = 'Logged in!'
    elif status == '201':
        qrSource = 'Confirm'

def send_QR():
    print("sending qrcode")
    cf = configparser.ConfigParser()
    if os.path.exists("./config/myconfig.conf"):
        cf.read("./config/myconfig.conf")
    else:
        cf.read("./config/config.conf")
    opts = cf.options("mailgun")
    api = cf.get("mailgun", "api")
    image = get_img()
    html = "<h2>扫一扫登录微信</h2><img src='" + image.get("img_url") + "'>"
    requests.post(
        "https://api.mailgun.net/v3/mail.dgcontinent.com/messages",
        auth=("api", api),
        data={"from": "Wechat 微信登录授权申请 <mailgun@test.com>",
              "to": ["frozen_tearz@163.com"],
              "subject": "Wechat 微信登录授权申请",
              "html": html
        }
    )

def main():
    itchat.auto_login(hotReload=True, qrCallback=qrCallback)
    while 1:
        Results = send_msg_to_user()
        if int(Results.get("status")):
            userMsg = "您好!\n您想搭乘" + Results.get("direction") + "的" + Results.get("line") + "公交车" + Results.get("msg")
            users=itchat.search_friends("Frazier")
            userName= users[0]['UserName']
            itchat.send(userMsg, toUserName=userName)
            time.sleep(60)
        else:
            pass
            time.sleep(5)


if __name__ == '__main__':
    main()
    
    