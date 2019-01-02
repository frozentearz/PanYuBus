#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import itchat
import json
import time
import ast

def get_img():
    image = {}
    url = "https://sm.ms/api/upload"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        'Postman-Token': "cf9bd2b3-1206-44b3-b136-621444b66ba7"
    }
    multipart_encoder = MultipartEncoder(
        fields = {
            'smfile': ('QR.png', open('./QR.png', 'rb'), 'image/png')
        },
        boundary = '-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    headers['Content-Type'] = multipart_encoder.content_type
    response = requests.post(url, data=multipart_encoder, headers=headers)
    
    if response.status_code != 200:
        print("图片上传失败")
    else:
        if response.text.get("code") != "success" :
            print("图片上传失败")
        else:
            image["img_url"] = response.text.get("data").get("url")
            image["del_url"] = response.text.get("data").get("delete")
    return image

def getDirection(bus):
    l = bus.get("l")
    startStation = l[0].get("n")
    endStation = l[len(l)-1].get("n")
    return startStation + "至" + endStation

def main():
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
            Results["msg"] = "还未达到，请耐心等候..."
        else: 
            Results["msg"] = "已到达" + stations[flag-before_num].get("n") + "，距您仅有 " + before_num + " 站，请做好上车准备！"
    return Results

def send_QR_to_email():
    image = get_img()
    print(image)
    html = "<h2>扫一扫登录微信</h2><img src='" + image.get("img_url") + "'>"
    requests.post(
        "https://api.mailgun.net/v3/mail.dgcontinent.com/messages",
        auth=("api", "fd5f270993f10b93397fb82231337e09-6b60e603-b16f5772"),
        data={"from": "Excited User <mailgun@mail.dgcontinent.com>",
              "to": ["frozen_tearz@163.com"],
              "subject": "Wechat 微信登录授权申请",
              "html": html})


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    while 1:
        Results = main()
        userMsg = "您好!\n您想搭乘" + Results.get("direction") + "的" + Results.get("line") + "公交车" + Results.get("msg")
        users=itchat.search_friends("林豪")
        userName= users[0]['UserName']
        itchat.send(userMsg, toUserName=userName)
        time.sleep(10)
    