#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import base64
import json

def b64_image(image):
    ##base64转image存储成图片
    strs = image
    imgdata = base64.b64decode(strs)
    file = open('1.jpg', 'wb')
    file.write(imgdata)
    file.close()

def get_code_uuid():
    ##获取image、UUID值
    code_url = "https://wiki.0-sec.org/api/user/captchaImage"
    code_image = requests.get(code_url)
    json_data = json.loads(code_image.content)
    base64_image = json_data['data']['img']
    base64_uuid = json_data['data']['uuid']
    b64_image(base64_image)

    return base64_uuid

def base64_api():
    img_path = "./1.jpg"
    with open(img_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": "你的api用户名", "password": "你的api用户密码", "image": b64}##你的验证码api账户
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        print("验证码识别抽风了，再执行一遍吧")

def login(uuid):
    username = "你的用户名"
    password = "你的用户密码"
    headers = {'Accept': 'application/json, text/plain, */*','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36','Content-Type': 'application/json;charset=UTF-8','Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
    url = "https://wiki.0-sec.org/api/user/login"
    login_data = {"account":username,"password":password,"code":base64_api(),"uuid":uuid}##字典
    data_json = json.dumps(login_data)##转json格式
    logins = requests.post(url=url,headers=headers,data=data_json)
    token = json.loads(logins.content)['data']['token']

    return token

def sign(token):
    headers = {'Zero-Token':token}
    url = "https://wiki.0-sec.org/api/profile"
    old_sign_data_json = requests.get(url=url,headers=headers)
    old_sign_data_credit = json.loads(old_sign_data_json.content)['data']['credit']

    url1 = "https://wiki.0-sec.org/api/front/user/sign"
    requests.post(url=url1, headers=headers)

    new_sign_data_json = requests.get(url=url, headers=headers)
    new_sign_data_credit = json.loads(new_sign_data_json.content)['data']['credit']

    if new_sign_data_credit > old_sign_data_credit:
        print("签到成功，您的当前积分为：",new_sign_data_credit)
    else:
        print("兄弟，你已经签到过了，你的积分为：",new_sign_data_credit)

def main():
    uuid = get_code_uuid()
    tokens = login(uuid)
    sign(tokens)

if __name__ == '__main__':
    main()






