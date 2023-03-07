# -*- coding: utf-8 -*-
import re
import time
import requests
from flask import request
from main import API, config

host = config["host"]["super_user_id"]
approve = config["others"]["approve"]
lover = config["host"]["lover"]
robot_name = config["host"]["robot_name"]
chatgpt_name = config["host"]["chatgpt_name"]
welcome_to_group = config["others"]["welcome_to_group"]
menu_1 = config["others"]["menu_1"]
menu_2 = config["others"]["menu_2"]
authorize_list = [host, lover]


def get_data():
    url_ = "https://github.com/luoguixin/qqrobot/archive/refs/heads/main.zip"
    response = requests.get(url_)
    return response.content


def menu():
    data = request.get_json()
    message = data['message']
    message_id = data['message_id']
    uid = data['user_id']

    if "菜单" == message:
        a = menu_1
        API.send(a)
        b = menu_2
        API.send(b)

    elif message.startswith(robot_name):
        new_message = message.replace(robot_name, "")
        if new_message == "":
            new_message = robot_name
        result = API.smart_reply(new_message)
        API.send(result)

    elif message.startswith("/"):
        new_message = message.replace("/", "")
        API.send(f"[CQ:tts,text={new_message}]")

    elif message.startswith("夸夸"):
        API.send(f"[CQ:poke,qq={uid}]")
        text = API.boast()
        API.send(f"[CQ:tts,text={text}]")

    elif "一言" == message:
        content = API.one_speak()
        API.send(content)

    elif "点歌" == message:
        API.send("请输入歌名")
        song_id = API.reply(message_id)
        if song_id == "回复超时":
            API.send(f"[CQ:at,qq={uid}] {song_id}")
        else:
            content, music_id = API.song(song_id)
            API.send(content)
            API.send(f"音乐链接:\nhttps://tsmusic24.tc.qq.com/{music_id}.mp3")

    elif "给我起个名" == message:
        name = API.random_name()
        img = API.head_img()
        API.send(f"[CQ:at,qq={uid}] 你的名字是{name}")
        API.send(f"[CQ:image,file={img}]")

    elif message.endswith("天气"):
        weather = API.weather(message)
        name = weather["name"]
        content = weather["data"]
        API.send(f"{name}\n{content}")

    elif message.startswith("搜索视频"):
        API.send("正在搜索中.....")
        data = API.video(message)
        if data == 0:
            API.send("没有这个视频")
        else:
            API.send(f"[CQ:video,file={data}]")

    elif "历史上的今天" == message:
        API.send("你要几条历史(最多5条)")
        new_message = API.reply(message_id)
        if new_message == "回复超时":
            API.send(f"[CQ:at,qq={uid}] {new_message}")
        else:
            data = API.history(new_message)
            API.send(data)

    elif message.startswith("查询域名状态"):
        try:
            name, data_qq, vx_data, time_s, now_time = API.url_query(message)
            API.send(
                f"网站名称:{name}\n单位性质:{data_qq}\n备案号:{vx_data}\n审核时间:{time_s}\n最近检查时间:{now_time}")
        except EnvironmentError as e:
            API.send(f"不在我国的域名(TMD自己不知道吗查查查)\n{e}")

    elif message.startswith("ping"):
        API.send("正在努力ping....")
        data = API.ping_url(message)
        API.send(data)

    elif message.startswith("度娘什么是"):
        data = API.baidu(message)
        API.send(data)

    elif message.startswith("翻译一下"):
        data = API.translate(message)
        API.send(f"意思是:{data}")

    elif message == "热门视频":
        API.send("你要几条热门视频(别太多避免刷屏(直接发数字就行))")
        new_message = API.reply(message_id)
        try:
            if int(new_message) > 5 or int(new_message) < 1:
                API.send("NTM有病是不是")
            else:
                data = API.hot_door(new_message)
                if data == 0:
                    API.send("你有半个吗？")
                else:
                    for i in data:
                        API.send(f'{i["title"]}\n热度:{i["hot"]}\n视频链接:{i["url"]}[CQ:image,file={i["pic"]}]')
        except EnvironmentError as e:
            API.send(f"哈哈哈哈小学没毕业是不是(实际上是因为{e})")

    elif message == "摸鱼日历":
        data = API.fish_day()
        API.send(f"[CQ:image,file={data}]")

    elif "网易云热评" == message:
        cover, content, name = API.random_music()
        API.send(f"歌曲名:{name}\n热评:{content}\n[CQ:image,file={cover}]")

    elif "黑丝" == message:
        img_url = API.picture()
        API.send(f"[CQ:image,file={img_url}]")

    elif "谁是你主人" == message:
        if uid == host:
            API.send("你就是呀")
        else:
            API.send(f"[CQ:at,qq={host}] 这就是我主人，我爱的主人")

    elif "安慰" in message:
        data = API.an_wei()
        API.send(data)

    elif "随机视频" == message:
        API.send("正在为你寻找有趣的视频")
        girl = API.girl_url()
        API.send(f"[CQ:video,file=http:{girl}]")

    elif robot_name == message:
        datas = API.abuse()
        API.send(f"[CQ:tts,text={datas}]")
        group_list = API.get_group_list()
        API.send(group_list["data"])

    elif message.startswith("快递查询"):
        API.send("正在查询.....")
        result = API.api_postmen(message)
        API.send(result)

    elif message == "今日新闻":
        API.send("你要看几条新闻")
        num = API.reply(message_id)
        result = API.api_news(num)
        API.send(result)

    elif message.startswith("缩短网址"):
        url = API.api_url(message)
        API.send(url)

    elif message.startswith("转发") and uid == host:
        temp, group_id_list = API.get_group_list()
        group_list = "\n".join(temp)
        API.send(f"请选择要转发的群\n一共有{len(group_id_list)}个群")
        API.send(group_list)
        API.send("输入数字选择转发的群, 以及要转发的内容并用/分隔开不要加空格")
        nums = API.reply(message_id)
        num = nums.split("/")[0]
        repost_message = nums.split("/")[-1]
        if int(num) < len(group_id_list):
            group_id = group_id_list[int(num) + 1]
            API.repost_group(repost_message, group_id)
            API.send(f"{num}已转发{repost_message}\n{group_id}")
        else:
            API.send("你最好是转发")

    elif message.startswith(chatgpt_name):
        if uid in authorize_list:
            new_message = str(re.findall(f"{chatgpt_name}(.*)", message)[0])
            result = API.askChatGPT(new_message)
            API.send(result)
        else:
            API.send("权限不够")

    elif message.startswith("授权") and uid == host:
        num = str(re.findall(r"\d+", message)[0])
        if num in authorize_list:
            API.send("已授权过了")
        else:
            authorize_list.append(int(num))
            API.send(f"已授权[CQ:at,qq={num}]")
    elif message.startswith("取消授权") and uid == host:
        num = str(re.findall(r"\d+", message)[0])
        if num in authorize_list:
            authorize_list.remove(int(num))
            API.send("已取消授权")
        else:
            API.send("该群友还没有权限")


def others():
    data = request.get_json()
    self_id = data["self_id"]
    if "target_id" in data:
        target_id = data["target_id"]  # 戳一戳参数就一个group_id 不一样
        if self_id == target_id:
            if "group_id" in data:
                sender_id = data["sender_id"]
                API.other_send_group(f"[CQ:poke,qq={sender_id}]")
                result = API.abuse()
                API.other_send_group(result)
            else:
                API.other_send_private("你好")
    elif "client" in data:
        client = data["client"]
        time2 = data["time"]
        s_l = time.localtime(time2)
        ts = time.strftime("%Y-%m-%d %H:%M:%S", s_l)
        with open(f"登录记录.txt", "a", encoding="gbk") as f:
            f.write(f"{ts}\n{client}\n")
    elif "notice_type" in data:
        notice_type = data["notice_type"]
        user_id = data["user_id"]
        if notice_type == "group_increase":
            API.other_send_group(f"[CQ:at,qq={user_id}]" + welcome_to_group)
    elif "flag" in data:
        flag = data["flag"]
        sub_type = data["sub_type"]
        group_id = data["group_id"]
        API.invite_group(flag, sub_type)
        if approve == "True":
            API.other_send_host(f"邀请类型为:{sub_type}\n群号为{group_id}\n已同意")
        else:
            API.other_send_host(f"邀请类型为:{sub_type}\n群号为{group_id}\n已拒绝")
