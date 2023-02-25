# -*- coding: utf-8 -*-
import random
import re
import openai
from flask import Flask, request
import requests
import menu
import sqlite3
import time
import json
import yaml

f = open("data.yaml", "r", encoding="utf-8")
config = yaml.safe_load(f)
f.close()
host = config["host"]["super_user_id"]
approve = config["others"]["approve"]
chatgpt_api = config["others"]["chatgpt_api"]
app = Flask(__name__)


class API:
    @staticmethod
    def send(message):
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
        url = "http://127.0.0.1:5700/send_msg"

        requests.get(url, params=params)

    @staticmethod
    def other_send_group(message):
        data = request.get_json()
        group_id = data["group_id"]
        params = {
            "auto_escape": False,
            "message": message,
            "group_id": group_id
        }
        url = "http://127.0.0.1:5700/send_group_msg"
        requests.get(url, params=params)

    @staticmethod
    def other_send_private(message, group_id=None):
        data = request.get_json()
        user_id = data["user_id"]
        params = {
            "auto_escape": False,
            "message": message,
            "user_id": user_id,
            "group_id": group_id
        }
        url = "http://127.0.0.1:5700/send_private_msg"
        requests.get(url, params=params)

    @staticmethod
    def other_send_host(message):
        params = {
            "auto_escape": False,
            "message": message,
            "user_id": host
        }
        url = "http://127.0.0.1:5700/send_private_msg"
        requests.get(url, params=params)

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
            except:
                if n == 58:
                    conn.commit()
                    conn.close()
                    return "回复超时"
                else:
                    time.sleep(1)
                    continue

    @staticmethod
    def smart_reply(message):
        try:
            url = f"https://open.drea.cc/bbsapi/chat/get?keyWord={message}"
            result = requests.get(url)
            js = result.text
            smart_result = json.loads(js)["data"]["reply"]
            return smart_result
        except:
            return "ok"

    @staticmethod
    def song(name):
        url = "https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg"
        headers = {"origin": "https://y.qq.com",
                   "referer": "https://y.qq.com/",
                   "accept": "application / json",
                   "accept-encoding": "gzip, deflate, br",
                   "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"}
        params = {
            "_": "1675271756352",
            "cv": "4747474",
            "ct": "24",
            "format": "json",
            "inCharset": "utf-8",
            "outCharset": "utf - 8",
            "notice": "0",
            "platform": "yqq.json",
            "needNewCode": "1",
            "uin": "0",
            "g_tk_new_20200303": "5381",
            "g_tk": "5381",
            "hostUin": "0",
            "is_xml": "0",
            "key": name
        }
        res = requests.get(url, headers=headers, params=params).json()
        try:
            music_qq_id = res["data"]["song"]["itemlist"][0]["id"]
            content = f"[CQ:music,type=qq,id={music_qq_id}]"
            return content, music_qq_id
        except EnvironmentError as e:
            return e

    @staticmethod
    def one_speak():
        url = "https://api.wrdan.com/hitokoto"
        rep = requests.get(url)
        js = rep.json()
        content = js["text"]
        return content

    @staticmethod
    def boast():
        url = "https://api.shadiao.pro/chp"
        rep = requests.get(url)
        data = rep.json()
        text = data["data"]["text"]
        return text

    @staticmethod
    def random_name():
        url = "http://yichen.api.z7zz.cn/api/xingming.php"
        rep = requests.get(url)
        name = rep.text.split("/>")[-1].replace("\n", "")
        return name

    @staticmethod
    def weather(message):
        location = str(re.findall(r"(.*)天气", message)[0]).replace(" ", "")
        url = "https://xiaoapi.cn/API/zs_tq.php"
        params = {
            "msg": location,
            "n": "1",
            "num": "20",
            "type": "cytq",
        }
        rep = requests.get(url, params)
        return rep.json()

    @staticmethod
    def video(message):
        messages = str(re.findall(r"搜索视频(.*)", message)[0]).replace(" ", "")
        n = random.choice([1, 2, 3, 4])
        url = "https://xiaoapi.cn/API/mv_sq.php"
        params = {
            "msg": messages,
            "n": n
        }
        try:
            rep = requests.get(url, params)
            data = rep.json()["url"][0]
            return data
        except:
            return 0

    @staticmethod
    def history(message):
        if "条" in message:
            message = str(message).replace("条", "")
        url = "https://xiaoapi.cn/API/lssdjt.php"
        params = {
            "type": message
        }
        rep = requests.get(url, params)
        data = rep.text
        return data

    @staticmethod
    def url_query(message):
        try:
            new_message = str(re.findall(r"查询域名状态(.*)", message)[0]).replace(" ", "")
            url = "https://xiaoapi.cn/API/zs_icp.php"
            params = {
                "url": new_message
            }
            rep = requests.get(url, params)
            url_name = rep.json()["网站名称"]
            data_qq = rep.json()["单位性质"]
            vx_data = rep.json()["备案号"]
            time_url = rep.json()["审核时间"]
            now_url_time = rep.json()["最近检测"]
            return url_name, data_qq, vx_data, time_url, now_url_time
        except:
            return 0

    @staticmethod
    def ping_url(message):
        new_message = str(re.findall(r"ping(.*)", message)[0]).replace(" ", "")
        url = "https://xiaoapi.cn/API/sping.php"
        params = {
            "url": new_message
        }
        rep = requests.get(url, params)
        return rep.text

    @staticmethod
    def baidu(message):
        new_message = str(re.findall(r"度娘什么是(.*)", message)[0]).replace(" ", "")
        url = "https://xiaoapi.cn/API/bk.php"
        params = {
            "msg": new_message,
            "m": "json",
            "type": "bd"
        }
        rep = requests.get(url, params)
        data = rep.json()["msg"]
        return data

    @staticmethod
    def translate(message):
        nem_message = str(re.findall(r"翻译一下(.*)", message)[0]).replace(" ", "")
        url = "https://api.vvhan.com/api/fy"
        params = {
            "text": nem_message
        }
        rep = requests.get(url, params)
        data = rep.json()["data"]["fanyi"]
        return data

    @staticmethod
    def hot_door(message):
        try:
            url = "https://api.vvhan.com/api/hotlist"
            params = {
                "type": "bili"
            }
            rep = requests.get(url, params)
            data = rep.json()["data"][0:int(message)]
            return data
        except:
            return 0

    @staticmethod
    def fish_day():
        url = "https://api.vvhan.com/api/moyu"
        params = {
            "type": "json"
        }
        rep = requests.get(url, params)
        data = rep.json()["url"]
        return data

    @staticmethod
    def random_music():
        url = "https://api.vvhan.com/api/reping"
        js = requests.get(url)
        data = js.json()
        cover = data["data"]["avatarUrl"]
        content = data["data"]["content"]
        name = data["data"]["name"]
        return cover, content, name

    @staticmethod
    def picture():
        url = "https://api.vvhan.com/api/mobil.girl"
        params = {
            "type": "json"
        }
        rep = requests.get(url, params)
        data = rep.json()
        img_url = data["imgurl"]
        return img_url

    @staticmethod
    def head_img():
        url = "https://api.vvhan.com/api/avatar?type=json"
        rep = requests.get(url)
        data = rep.json()["avatar"]
        return data

    @staticmethod
    def an_wei():
        url = "https://v.api.aa1.cn/api/api-wenan-anwei/index.php"
        params = {
            "type": "json"
        }
        rep = requests.get(url, params)
        data = rep.json()["anwei"]
        return data

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
    def abuse():
        n = random.choice([1, 2, 3, 4, 5])
        url = "https://v.api.aa1.cn/api/api-wenan-ktff/index.php"
        params = {
            "type": n
        }
        rep = requests.get(url, params)
        js = rep.text.split(":")[2].replace('"}', "").replace('"', "")
        return js

    @staticmethod
    def host_start(message):
        url = "http://127.0.0.1:5700/send_private_msg"
        params = {
            "user_id": config.get("host", "super_user_id"),
            "message": message,
            "auto_escape": False
        }
        requests.get(url, params)

    @staticmethod
    def api_postmen(message):
        new_message = str(re.findall("快递查询(.*)", message)[0])
        if new_message.isdigit():
            url = "https://xiaoapi.cn/API/zs_kd.php"
            params = {
                "num": new_message
            }
            resp = requests.get(url, params=params)
            result = resp.json()
            return result["msg"]
        else:
            return "请输入正确的快递单号"

    @staticmethod
    def api_news(message):
        new_message = str(re.findall(r"[1-9]", message)[0])
        if new_message.isdigit():
            url = "https://xiaoapi.cn/API/zs_xw.php"
            params = {
                "num": message
            }
            resp = requests.get(url, params=params)
            result = resp.json()["msg"]
            return result
        else:
            return "你没学过数学吗？"

    @staticmethod
    def api_url(message):
        new_message = str(re.findall("缩短网址(.*)", message)[0]).replace(" ", "")
        url = "https://xiaoapi.cn/API/dwz.php"
        params = {
            "url": new_message
        }
        resp = requests.get(url, params=params)
        return resp.text

    @staticmethod
    def get_group_list():
        url = "http://127.0.0.1:5700/get_group_list"
        params = {
            "no_cache": False
        }
        group_list = requests.get(url, params=params)
        result = group_list.json()["data"]
        temp = []
        group_id_list = []
        for i in result:
            temp.append(f'{i["group_name"]}:{i["group_id"]}')
            group_id_list.append(i["group_id"])
        return temp, group_id_list

    @staticmethod
    def repost_group(message, group_id):
        params = {
            "auto_escape": False,
            "message": message,
            "group_id": group_id
        }
        url = "http://127.0.0.1:5700/send_group_msg"
        requests.get(url, params=params)

    @staticmethod
    def invite_group(flag, sub_type):
        if approve == "True":
            params = {
                "flag": flag,
                "sub_type": sub_type,
                "approve": True,
            }
            url = "http://127.0.0.1:5700/set_group_add_request"
            requests.get(url, params=params)
        else:
            params = {
                "flag": flag,
                "sub_type": sub_type,
                "approve": False,
                "reason": "我是机器人我不想进群，也不同意陌生人加群"
            }
            url = "http://127.0.0.1:5700/set_group_add_request"
            requests.get(url, params=params)

    @staticmethod
    def askChatGPT(question):
        try:
            openai.api_key = chatgpt_api
            prompt = question
            model_engine = "text-davinci-003"

            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )

            message = completions.choices[0].text
            return message
        except:
            return "AI正在维护中请联系开发者"

    @staticmethod
    def Gpt_forchange(msg):
        url = "https://api.forchange.cn/"
        params = {'prompt': f"Human:{msg}↵AI:", 'tokensLength': 9}
        try:
            if re.search(r'^\s+', msg):
                msg = re.sub(r'^\s+', '', msg)
            if not re.search(r'\S', msg):
                return "！"
            res = requests.get(url, params=params).json()
            res = res['choices'][0]['text']
            if re.search(r'^\s+', res):
                res = re.sub(r'^\s+', '', res)
            if "访问人数" in res:
                return "当前访问人数过多"
            if "sorry" in res:
                return "抱歉你的问题被吞了"
            if "维护" in res:
                return "前方的区域以后再来探索吧"
            return res
        except Exception as E:
            return f"我还不知道问题的答案{E}"


@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    if data['post_type'] == 'message':
        API.save_message()
        message = data['message']
        print(message)
        menu.menu()
    else:
        menu.others()
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5701)
