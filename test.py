# -*- coding: utf-8 -*-

import itchat
import time

def main():
    itchat.auto_login(hotReload=True, enableCmdQR=True)
    count = 0
    while 1:
        count += 1
        users=itchat.search_friends("Frazier")
        userName= users[0]['UserName']
        itchat.send("测试" + str(count), toUserName=userName)
        time.sleep(10)

if __name__ == '__main__':
    main()