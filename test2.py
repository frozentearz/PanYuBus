#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import random
import json
from requests_toolbelt import MultipartEncoder

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

def main():
    send_simple_message()

if __name__ == '__main__':
    main()