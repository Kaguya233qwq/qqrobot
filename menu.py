from flask import request
from main import API
from configparser import ConfigParser
config = ConfigParser()
config.read(r"info.ini", encoding="utf-8")
host = config.get("host", "super_user_id")


def menu():
    data = request.get_json()
    message = data['message']
    message_id = data['message_id']
    uid = data['user_id']
    self_id = data["self_id"]

    if "菜单" == message:
        a = """----------菜单------------
1.人工智障梦幻（触发词梦幻）
2.转语音（触发词/）
3.彩虹屁（触发词夸夸xxx）
4.一言（触发词一言）
5.点歌（触发词点歌）
6.随机姓名（触发词给我起个名）
7.天气查询（触发词xxx天气）
8.网易云热评
提示:还有第二页(输入第二页查看)"""
        API.send(a)
        new_message = API.reply(message_id)
        if new_message == "第二页":
            b = """9.视频搜索（触发词搜索视频xxx）
10.历史上的今天（触发词历史上的今天）
11.域名状态查询（查询域名状态xxx.com）
12.ping（触发词ping xxx.xxx.xxx）
13.度娘（度娘什么是xxx）
14.翻译（翻译一下）
15.b站热门视频（触发词b站热门视频）
16.摸鱼日历
"""
            API.send(b)
        else:
            new_data = API.reply(message_id)
            if "第二页" in new_data:
                API.send("没了")

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
            content = API.song(song_id)
            API.send(content)

    elif "给我起个名" == message:
        name = API.random_name()
        img = API.head_img()
        API.send(f"[CQ:at,qq={uid}] 你的名字是{name}")
        API.send(f"[CQ:image,file={img}]")

    elif message.endswith("天气"):
        weather = API.weather(message)
        new_data = weather.split("\n")[0:3]
        new_weather = "\n".join(new_data)
        API.send(new_weather)

    elif message.startswith("搜索视频"):
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
            name, data_qq, vx_data, time, now_time = API.url_query(message)
            API.send(f"网站名称:{name}\n单位性质:{data_qq}\n备案号:{vx_data}\n审核时间:{time}\n最近检查时间:{now_time}")
        except:
            API.send("不在我国的域名(TMD自己不知道吗查查查)")

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
        except:
            API.send("哈哈哈哈小学没毕业是不是")

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
        if uid == int(host):
            API.send("好的，主人")
        else:
            API.send("你是什么东西!!!")

    elif "安慰" in message:
        data = API.anwei()
        API.send(data)

    elif "随机视频" == message:
        girl = API.girl_url()
        API.send(f"[CQ:video,file=http:{girl}]")

    elif "文心" in message:
        datas = API.abuse()
        API.send(f"[CQ:tts,text={datas}]")

    else:
        pass
    return "OK"
