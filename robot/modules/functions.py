import sqlite3
import time

import clueai
import requests
from fake_useragent import UserAgent
from flask import request

from robot.util.config import Config

UA = UserAgent()


class API:

    @staticmethod
    def abuse():  # TODO:一个一言api
        url = "https://xiaoapi.cn/API/yiyan.php"
        resp = requests.get(url)
        return resp.text

    @staticmethod
    def picture():  # TODO:一个图片api返回随机图片链接
        url = "https://img.xjh.me/random_img.php?return=json"
        esp = requests.get(url)
        url_img = esp.json()["img"]
        urls_n_img = f"https:{url_img}"
        return urls_n_img

    @staticmethod
    def girl_url():  # TODO: 一个api返回视频链接，相当于随机视频
        url = "https://v.api.aa1.cn/api/api-girl-11-02/index.php"
        params = {
            "type": "json"
        }
        rep = requests.get(url, params)
        data = rep.json()["mp4"]
        return data

    @staticmethod
    def bilbil_content(oid):  # TODO: 获取某个up主的个人主页信息
        url = f"https://api.bilibili.com/x/v2/reply?&type=1&pn=1&oid={oid}"
        headers = {"user-agent": UA.chrome}
        resp = requests.get(url, headers=headers)
        num = len(resp.json()["data"]["replies"])
        contents = []
        for i in range(num):
            content = resp.json()["data"]["replies"][i]["content"]["message"]
            contents.append(content)
        return contents

    @staticmethod
    def invite_group(flag, sub_type):
        if Config.APPROVE:
            params = {
                "flag": flag,
                "sub_type": sub_type,
                "approve": True,
            }
            url = f"{Config.PORT}/set_group_add_request"
            requests.get(url, params=params)
        else:
            params = {
                "flag": flag,
                "sub_type": sub_type,
                "approve": False,
                "reason": "我是机器人我不想进群，也不同意陌生人加群"
            }
            url = f"{Config.PORT}/set_group_add_request"
            requests.get(url, params=params)

    @staticmethod
    def up_fans_nums(uid=Config.MONITOR):
        url = f"https://api.bilibili.com/x/relation/stat?vmid={uid}"
        resp = requests.get(url)
        return resp.json()["data"]["follower"]

    @staticmethod
    def send_mail(user_name, user_id, title, message):
        url = "https://api.wer.plus/api/qqmail"
        params = {
            "me": "luoguixinduide@foxmail.com",
            "name": user_name,
            "to": f"{user_id}@qq.com",
            "title": title,
            "text": message,
            "key": "nzlbpmnflrjcdfdd"
        }

        resp = requests.get(url, params=params)
        return resp.json()["data"]["status"]

    @staticmethod
    def free_gpt(message):
        # initialize the Clueai Client with an API Key
        cl = clueai.Client(Config.CHATGPT_API, check_api_key=True)
        prompt = message
        # generate a prediction for a prompt
        # 需要返回得分的话，指定return_likelihoods="GENERATION"
        prediction = cl.generate(
            model_name='ChatYuan-large',
            prompt=prompt)

        # print the predicted text
        return prediction.generations[0].text

    @staticmethod
    def save_message():  # TODO:这个函数用于储存消息，用于机器人于用户交互
        data = request.get_json()
        uid = data['user_id']
        message = data['message']
        message_id = data['message_id']
        send_time = data['time']
        message_type = data['message_type']
        if message_type == 'group':
            group_id = data['group_id']
        else:
            group_id = "null"
        conn = sqlite3.connect("bot.db")
        c = conn.cursor()
        c.execute(
            "insert into message(QQ, message, message_id, send_time, message_type, group_id) values (?, ?, ?, ?, ?, ?)",
            (uid, message, message_id, send_time, message_type, group_id))
        conn.commit()
        conn.close()

    @staticmethod
    def xiao_rou(message):
        url = f"https://v1.apigpt.cn/?q={message}&apitype=sql"
        data = requests.get(url)
        return data.json()["ChatGPT_Answer"]

    @staticmethod
    def reply(message_id):  # TODO:与前面的save_message函数联用,这个需要传入message_id，返回信息
        conn = sqlite3.connect("bot.db")
        c = conn.cursor()
        c.execute("SELECT * FROM message WHERE message_id = ?", (message_id,))
        results = c.fetchone()
        QQ = results[1]
        ID = results[0]
        group_id = results[6]
        message_type = results[5]
        num = ID + 1
        n = 0
        for i in range(60):
            n += 1
            try:
                c.execute("SELECT * FROM message WHERE id = ?", (num,))
                results = c.fetchone()
                new_QQ = results[1]
                new_group_id = results[6]
                new_message_type = results[5]
                if message_type == new_message_type == 'group':
                    if int(new_QQ) == int(QQ):
                        if int(new_group_id) == int(group_id):
                            new_message = results[2]
                            conn.commit()
                            conn.close()
                            return new_message
                        else:
                            num += 1
                            if n == 58:
                                conn.commit()
                                conn.close()
                                return "回复超时"
                            else:
                                time.sleep(1)
                                continue
                    else:
                        num += 1
                        if n == 58:
                            conn.commit()
                            conn.close()
                            return "回复超时"
                        else:
                            time.sleep(1)
                            continue
                elif message_type == new_message_type == 'private':
                    if int(new_QQ) == int(QQ):
                        new_message = results[2]
                        conn.commit()
                        conn.close()
                        return new_message
                    else:
                        num += 1
                        if n == 58:
                            conn.commit()
                            conn.close()
                            return "回复超时"
                        else:
                            time.sleep(1)
                            continue
                else:
                    num += 1
                    if n == 58:
                        conn.commit()
                        conn.close()
                        return "回复超时"
                    else:
                        time.sleep(1)
                        continue
            except TypeError:
                if n == 58:
                    conn.commit()
                    conn.close()
                    return "回复超时"
                else:
                    time.sleep(1)
                    continue
