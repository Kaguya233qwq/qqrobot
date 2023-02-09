import random
import re
from flask import Flask, request
import requests
import menu
import sqlite3
import time
import json
from wsgiref.simple_server import make_server
from configparser import ConfigParser
import wenxin_api  # 可以通过"pip install wenxin-api"命令安装
from wenxin_api.tasks.free_qa import FreeQA
config = ConfigParser()
config.read(r"info.ini", encoding="utf-8")
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
            return content
        except:
            pass
        return "ok"

    @staticmethod
    def one_speak():
        url = "https://api.wrdan.com/hitokoto"  # 一言
        rep = requests.get(url)
        js = rep.json()
        content = js["text"]
        return content

    @staticmethod
    def boast():
        url = "https://api.shadiao.pro/chp"  # 彩虹屁
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
        url = "http://yichen.api.z7zz.cn/api/qqtq.php"
        params = {
            "msg": location
        }
        rep = requests.get(url, params)
        return rep.text

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
    def wen_xin(message):
        wenxin_api.ak = config.get("other", "wenxin_api.ak")
        wenxin_api.sk = config.get("other", "wenxin_api.sk")
        input_dict = {
            "text": f"问题:{message}\n回答:",
            "seq_len": 512,
            "topp": 0.5,
            "penalty_score": 1.2,
            "min_dec_len": 2,
            "min_dec_penalty_text": "。?：！[<S>]",
            "is_unidirectional": 0,
            "task_prompt": "qa",
            "mask_type": "paragraph"
        }
        rst = FreeQA.create(**input_dict)
        return rst["result"]

    @staticmethod
    def host_start(message):
        url = "http://127.0.0.1:5700/send_private_msg"
        params = {
            "user_id": config.get("host", "super_user_id"),
            "message": message,
            "auto_escape": False
        }
        requests.get(url, params)


@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    print(data)
    if data['post_type'] == 'message':
        API.save_message()
        message = data['message']
        print(message)
        menu.menu()
    else:
        pass
    return "OK"


if __name__ == '__main__':
    print("服务器启动成功")
    API.host_start("主人我启动成功了哦")
    server = make_server('0.0.0.0', 5701, app)
    server.serve_forever()
    app.run()
