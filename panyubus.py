# -*- coding: utf-8 -*-

import requests
import itchat
import json
import time
import ast

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
        if dict.get("code") == 200 and dict.get("msg") == "ok":
            bus = dict.get("data").get("bus")
            Results["line"] = bus.get("rn")
            Results["direction"] = getDirection(bus)
            stations = bus.get("l")
            for station in stations:
                if station.get("n") == my_station:
                    flag = stations.index(station)
            bus_status = stations[flag-before_num].get("bus_comming")
            if len(bus_status.get("bl")) == 0 and len(bus_status.get("bbl") == 0):
                Results["msg"] = "还未达到，请耐心等候..."
            else: 
                Results["msg"] = "已到达" + stations[flag-before_num].get("n") + "，距您仅有 " + before_num + " 站，请做好上车准备！"
    except Exception as e:
        print("API数据获取失败！ Error: ")
        print(e)
    return Results

def getDirection(bus):
    l = bus.get("l")
    startStation = l[0].get("n")
    endStation = l[len(l)-1].get("n")
    return startStation + "至" + endStation

if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=True)
    while 1:
        Results = main()
        print(Results)
        userMsg = "您好!\n您想搭乘" + Results.get("direction") + "的" + Results.get("line") + "公交车" + Results.get("msg")
        users=itchat.search_friends("Frazier")
        userName= users[0]['UserName']
        itchat.send(userMsg, toUserName=userName)
        time.sleep(10)
    