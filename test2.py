#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import requests
import random
import itchat
import json
import time
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


def send_QR():
    image = get_img()
    print(image)
    html = "<h2>扫一扫登录微信</h2><img src='" + image.get("img_url") + "'>"

    return requests.post(
        "https://api.mailgun.net/v3/mail.dgcontinent.com/messages",
        auth=("api", "fd5f270993f10b93397fb82231337e09-6b60e603-b16f5772"),
        data={"from": "Excited User <mailgun@mail.dgcontinent.com>",
              "to": ["frozen_tearz@163.com"],
              "subject": "Wechat 微信登录授权申请",
              "html": html})

def wechat_login():
    itchat.auto_login()

def main():
    t1 = threading.Thread(target=wechat_login)
    t2 = threading.Thread(target=send_QR)

    t1.start()
    while True:
        if os.path.exists("./QR.png"):
            t2.start()
        time.sleep(0.5)
        break;

    print("finished")

if __name__ == '__main__':
    # main()
    print(send_QR())
    # print(get_img()) 