import datetime
import sqlite3
import time
import redis
import yaml
import menu
from flask import Flask, request
import requests
from threading import Timer
import clueai
from fake_useragent import UserAgent

ua = UserAgent()

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
f = open("data.yaml", "r", encoding="utf-8")
config = yaml.safe_load(f)
f.close()
chatgpt_api = config["initialization"]["chatgpt_api"]
monitor = config["initialization"]["monitor"]
approve = config["initialization"]["approve"]
port = config["initialization"]["port"]
mail_key = config["initialization"]["mail_key"]
mail_address = config["initialization"]["mail_address"]
app = Flask(__name__)


class API:
    def __init__(self):
        self.port = port
        self.host = config["initialization"]["host"]
        self.api_keys = config["initialization"]["api_key"]
        self.chatgpt_api = chatgpt_api
        self.api_secrets = config["initialization"]["api_secret"]
        self.approve = approve
        self.monitor = monitor
        self.monitor_group = config["initialization"]["monitor_group"]

    def send(self, message):
        data = request.get_json()
        message_type = data['message_type']
        if 'group' == message_type:
            group_id = data['group_id']
            params = {
                "message_type": message_type,
                "group_id": str(group_id),
                "message": message,
                "auto_escape": False
            }
        else:
            user_id = data['user_id']
            params = {
                "message_type": message_type,
                "user_id": str(user_id),
                "message": message,
                "auto_escape": False
            }
        url = f"{self.port}/send_msg"
        requests.get(url, params=params)

    def other_send_group(self, message):
        group_id = self.monitor_group
        params = {
            "auto_escape": False,
            "message": message,
            "group_id": group_id
        }
        url = f"{self.port}/send_group_msg"
        requests.get(url, params=params)

    def other_send_private(self, message, group_id=None):
        data = request.get_json()
        user_id = data["user_id"]
        params = {
            "auto_escape": False,
            "message": message,
            "user_id": user_id,
            "group_id": group_id
        }
        url = f"{self.port}/send_private_msg"
        requests.get(url, params=params)

    @staticmethod
    def abuse():
        url = "https://xiaoapi.cn/API/yiyan.php"
        resp = requests.get(url)
        return resp.text

    def other_send_host(self, message):
        params = {
            "auto_escape": False,
            "message": message,
            "user_id": self.host
        }
        url = f"{self.port}/send_private_msg"
        requests.get(url, params=params)

    @staticmethod
    def picture():
        url = "https://img.xjh.me/random_img.php?return=json"
        esp = requests.get(url)
        url_img = esp.json()["img"]
        urls_n_img = f"https:{url_img}"
        return urls_n_img

    def other_send_group_poke(self, message):
        data = request.get_json()
        group_id = data["group_id"]
        params = {
            "auto_escape": False,
            "message": message,
            "group_id": group_id
        }
        url = f"{self.port}/send_group_msg"
        requests.get(url, params=params)

    @staticmethod
    def girl_url():
        url = "https://v.api.aa1.cn/api/api-girl-11-02/index.php"
        params = {
            "type": "json"
        }
        rep = requests.get(url, params)
        data = rep.json()["mp4"]
        return data

    @staticmethod
    def bilbil_content(oid):
        url = f"https://api.bilibili.com/x/v2/reply?&type=1&pn=1&oid={oid}"
        headers = {"user-agent": ua.chrome}
        resp = requests.get(url, headers=headers)
        num = len(resp.json()["data"]["replies"])
        contents = []
        for i in range(num):
            content = resp.json()["data"]["replies"][i]["content"]["message"]
            contents.append(content)
        return contents

    def invite_group(self, flag, sub_type):
        if self.approve:
            params = {
                "flag": flag,
                "sub_type": sub_type,
                "approve": True,
            }
            url = f"{self.port}/set_group_add_request"
            requests.get(url, params=params)
        else:
            params = {
                "flag": flag,
                "sub_type": sub_type,
                "approve": False,
                "reason": "我是机器人我不想进群，也不同意陌生人加群"
            }
            url = f"{self.port}/set_group_add_request"
            requests.get(url, params=params)

    @staticmethod
    def up_fans_nums(uid=monitor):
        url = f"https://api.bilibili.com/x/relation/stat?vmid={uid}"
        resp = requests.get(url)
        return resp.json()["data"]["follower"]

    @staticmethod
    def send_mail(user_name, user_id, title, message):
        url = "https://api.wer.plus/api/qqmail"
        params = {
            "me": mail_address,
            "name": user_name,
            "to": f"{user_id}@qq.com",
            "title": title,
            "text": message,
            "key": mail_key
        }

        resp = requests.get(url, params=params)
        return resp.json()["data"]["status"]

    def free_gpt(self, message):
        # initialize the Clueai Client with an API Key
        cl = clueai.Client(self.chatgpt_api, check_api_key=True)
        prompt = message
        # generate a prediction for a prompt
        # 需要返回得分的话，指定return_likelihoods="GENERATION"
        prediction = cl.generate(
            model_name='ChatYuan-large',
            prompt=prompt)

        # print the predicted text
        return prediction.generations[0].text

    @staticmethod
    def save_message():
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
    def reply(message_id):
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


@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    api = API()
    print(data)
    if data['post_type'] == 'message':
        api.save_message()
        message = data['message']
        print(message)
        menu.menu()
    else:
        menu.other_menu()
    return "ok"


def time_printer():
    api = API()
    curr_time = datetime.datetime.now()
    timestamp = curr_time.hour
    time_min = curr_time.minute
    time_second = curr_time.second
    times = f"{timestamp}:{time_min}:{time_second}"
    if times == "12:0:0":
        api.other_send_host(f"中午啦，吃午饭了吗？注意开支哦")
    elif times == "5:0:0":
        api.other_send_group(f"[CQ:at,qq={monitor}]早点休息哦！")
    elif times == "7:0:0":
        api.other_send_host("早上好主人")
        url = "https://xiaoapi.cn/API/zs_xw.php?num=20"
        resp = requests.get(url)
        msg = resp.json()["msg"]
        api.other_send_host(msg)
        api.other_send_group("今日新闻\n" + msg)
    loop_monitor()


def loop_monitor():
    t = Timer(1, time_printer)
    t.start()


if __name__ == '__main__':
    f2 = open("qq_login/config.yml", "r", encoding="utf-8")
    config2 = yaml.safe_load(f2)
    f2.close()
    loop_monitor()
    app.run(host='0.0.0.0', port=int(config2["servers"][0]["http"]["post"][-1]["url"].split(":")[-1].replace("/", "")))
