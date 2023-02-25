# -*- coding: utf-8 -*-
import re
import tempfile
import time
import zipfile
import requests
from flask import request
from main import API
from configparser import ConfigParser

config = ConfigParser()
config.read(r"info.ini", encoding="utf-8")
host = config.get("host", "super_user_id")
lover = config.get("host", "lover")
approve = config.get("others", "approve")
authorize_list = [host, lover]


def get_data():
    url_ = "https://github.com/luoguixin/update/archive/refs/heads/main.zip"
    response = requests.get(url_)
    return response.content


def menu():
    data = request.get_json()
    message = data['message']
    message_id = data['message_id']
    uid = data['user_id']

    if "菜单" == message:
        a = """----------菜单------------
1.人工智障梦幻（触发词"梦幻"）
2.转语音（触发词"/"）
3.彩虹屁（触发词"夸夸xxx"）
4.一言（触发词"一言"）
5.点歌（触发词"点歌"）
6.随机姓名（触发词"给我起个名"）
7.天气查询（触发词"xxx天气"）
8.网易云热评"""
        API.send(a)
        b = """9.视频搜索（触发词搜索视频xxx）
    10.历史上的今天（触发词"历史上的今天"）
    11.域名状态查询（"查询域名状态xxx.com"）
    12.ping（触发词"ping xxx.xxx.xxx"）
    13.度娘（"度娘什么是xxx"）
    14.翻译（"翻译一下"）
    15.b站热门视频（触发词"b站热门视频"）
    16.摸鱼日历
    """
        API.send(b)

    elif message.startswith("梦幻"):
        new_message = message.replace("梦幻", "")
        if new_message == "":
            new_message = "梦幻"
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

    elif "叫我主人" == message:
        user_id = data["user_id"]
        if uid == int(host):
            API.send("好的，主人")
        else:
            API.send(f"[CQ:at,qq={user_id}]你是什么东西!!!")

    elif "安慰" in message:
        data = API.an_wei()
        API.send(data)

    elif "随机视频" == message:
        API.send("正在为你寻找有趣的视频")
        girl = API.girl_url()
        API.send(f"[CQ:video,file=http:{girl}]")

    elif "云梦" == message:
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

    elif message.startswith("转发") and uid == int(host):
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

    elif message.startswith("文心"):
        if str(uid) in authorize_list:
            new_message = str(re.findall("文心(.*)", message)[0])
            result = API.askChatGPT(new_message)
            API.send(result)
        else:
            API.send("权限不够")

    elif message.startswith("授权") and uid == int(host):
        num = str(re.findall(r"\d+", message)[0])
        if num in authorize_list:
            API.send("已授权过了")
        else:
            authorize_list.append(num)
            API.send(f"已授权[CQ:at,qq={num}]")
    elif message.startswith("取消授权") and uid == int(host):
        num = str(re.findall(r"\d+", message)[0])
        if num in authorize_list:
            authorize_list.remove(num)
            API.send("已取消授权")
        else:
            API.send("该群友还没有权限")

    elif "检查更新" == message and uid == int(host):
        f1 = open("data.txt", "r", encoding="utf-8")
        old_time = f1.readline()
        f1.close()
        url_api = "https://api.github.com/repos/luoguixin/update"
        resp = requests.get(url_api)
        update_time = resp.json()["updated_at"]
        if old_time == update_time:
            API.send("无需更新")
        else:
            API.send("正在更新中")
            f2 = open("data.txt", "w", encoding="utf-8")
            f2.write(update_time)
            f2.close()
            data = get_data()  # data为byte字节
            _tmp_file = tempfile.TemporaryFile()  # 创建临时文件
            _tmp_file.write(data)
            zf = zipfile.ZipFile(_tmp_file, mode='r')
            for names in zf.namelist():
                f = zf.extract(names, '../')  # 解压到zip目录文件下
                API.send(f"已更新{f}")
            API.send("更新完成!!!!")
            zf.close()

    elif message.startswith("云梦"):
        new_message = str(re.findall("云梦(.*)", message)[0])
        result = API.Gpt_forchange(new_message)
        API.send(result)


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
        with open(f"登录记录.txt", "a", encoding="utf-8") as f:
            f.write(f"{ts}\n{client}\n")
    elif "notice_type" in data:
        notice_type = data["notice_type"]
        user_id = data["user_id"]
        if notice_type == "group_increase":
            API.other_send_group(f"[CQ:at,qq={user_id}]新来的你先回答以下问题\n1.性别:\n2.年龄:\n3.所在城市:")
    elif "flag" in data:
        flag = data["flag"]
        sub_type = data["sub_type"]
        group_id = data["group_id"]
        API.invite_group(flag, sub_type)
        if approve == "True":
            API.other_send_host(f"邀请类型为:{sub_type}\n群号为{group_id}\n已同意")
        else:
            API.other_send_host(f"邀请类型为:{sub_type}\n群号为{group_id}\n已拒绝")
