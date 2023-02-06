import requests
from flask import Flask, request
from main import API


def menu():
    data = request.get_json()
    message = data['message']
    message_id = data['message_id']
    message_type = data['message_type']
    uid = data['user_id']

    if "菜单" == message:
        a = "找云深不知处"
        API.send(a)
    elif "私聊命令" == message:
        a = '暂无'
        API.send(a)
    elif '测试交互' == message:
        API.send("请输入你的身高")
        messages = API.reply(message_id)
        if "超时" in messages:
            if message_type == 'group':
                API.send("[CQ:at,qq="+str(uid)+"]"+"回复超时")
            else:
                API.send("回复超时")
        else:
            API.send("你的身高为:" + str(messages))
    elif message.startswith("梦幻"):
        new_message = message.replace("梦幻", "")
        if new_message == "":
            new_message = "梦幻"
        result = API.smart_reply(new_message)
        API.send(f"[CQ:tts,text={result}]")

    elif message.startswith("/"):
        new_message = message.replace("/", "")
        API.send(f"[CQ:tts,text={new_message}]")

    elif message.startswith("f"):
        new_message = message.replace("f", "")
        API.send(f"[CQ:face,id={new_message}]")

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

    elif message == "test":
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

    else:
        pass
    return "OK"
