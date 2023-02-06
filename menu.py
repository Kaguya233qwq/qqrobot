from flask import Flask, request
from main import API


def menu():
    data = request.get_json()
    message = data['message']
    message_id = data['message_id']
    uid = data['user_id']

    if "菜单" == message:
        a = """----------菜单------------
1.人工智障梦幻（触发词梦幻）
2.转语音（触发词/）
3.彩虹屁（触发词夸夸xxx）
4.一言（触发词一言）
5.点歌（触发词点歌）
6.随机姓名（触发词给我起个名）
7.天气查询（触发词xxx天气）
8.视频搜索（触发词搜索视频xxx）
9.历史上的今天（触发词历史上的今天）
10.域名状态查询（查询域名状态xxx.com）
11.ping（触发词pingxxx.xxx.xxx）
12.度娘（度娘什么是xxx）
13.翻译（翻译一下）
14.b站热门视频（触发词b站热门视频）
15.摸鱼日历
16.网易云热评"""
        API.send(a)

    elif message.startswith("梦幻"):
        new_message = message.replace("梦幻", "")
        if new_message == "":
            new_message = "梦幻"
        result = API.smart_reply(new_message)
        API.send(f"[CQ:tts,text={result}]")

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
        content = API.song(song_id)
        API.send(content)

    elif "给我起个名" == message:
        name = API.random_name()
        API.send(f"[CQ:at,qq={uid}] 你的名字是{name}")

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

    else:
        pass
    return "OK"
