import os
import random
import re
from ..modules import selenuims
import clueai
from flask import request
import psutil
import platform
from robot.plugins import plugin
from clueai.error import ClueaiError
from requests.exceptions import JSONDecodeError

from robot.message.api import send, other_send_group_poke, other_send_host
from robot.modules.functions import API
from robot.util.config import Config


temp = []
host_temp = [Config.HOST]
group_list = []


def menu():
    api = API()
    data = request.get_json()
    message = data['message']
    message_type = data["message_type"]
    user_id = data["user_id"]
    self_id = data["self_id"]
    random_reply(message)
    if message == Config.BOT_NAME:
        result = api.abuse()
        send(result)

    elif message.startswith(Config.BOT_NAME):
        group_id = data["group_id"]
        if str(user_id) in temp:
            send("你好像被加入黑名单了你想想你干了什么")
        elif "机器人" in message:
            send(f"我是真人，这年头谁用机器人啊\n{Config.OTHER_INFO}")
        elif message.startswith(f"{Config.BOT_NAME}查看视频评论"):
            oid = str(re.findall(f"{Config.BOT_NAME}查看视频评论(.*)", message)[0])
            content = api.bilbil_content(oid)
            send("\n".join(content))
        elif "检查系统" in message:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
            mem = psutil.virtual_memory()
            mem_usage = mem.percent
            disk_usage = psutil.disk_usage("/")
            send(
                f'当前cup使用率为:{cpu_percent}%\n当前cpu占用为详情为'
                f'\n{cpu_percents}\nRAM占用率为:{mem_usage}%\n磁盘占用率:{disk_usage.percent}%')
            send(f"操作系统及版本信息{platform.platform()}\n获取系统版本号{platform.version()}"
                 f"\n获取系统名称{platform.system()}\n处理器类型{platform.processor()}")
        elif group_id not in group_list:
            new_message = str(re.findall(f"{Config.BOT_NAME}(.*)", message)[0])
            result = api.xiao_rou(new_message)
            send(result)

    elif message_type == "private":
        result = api.free_gpt(message)
        send(result)

    elif f"[CQ:at,qq={self_id}]" in message and str(user_id) not in temp:
        new_message = message.replace(f"[CQ:at,qq={self_id}]", "")
        group_id = data["group_id"]
        if str(user_id) in temp:
            send("你好像被加入黑名单了你想想你干了什么")
        elif "机器人" in message:
            send("我是真人，我只是模仿机器人")
        elif group_id not in group_list:
            try:
                result = api.free_gpt(new_message)
                send(result)
            except ClueaiError:
                send("你他妈的")

    elif message.startswith(Config.BOT_NAME) and str(user_id) not in temp:
        new_message = message.replace(Config.BOT_NAME, "")
        result = api.free_gpt(new_message)
        send(result)

    elif random.random() < Config.RANDOM:
        if "为什么" in message:
            result = api.free_gpt(message)
            send(result)

    elif message.startswith("up粉丝数"):
        uid = str(re.findall("up粉丝数(.*)", message)[0])
        if uid == "":
            fans_num = api.up_fans_nums()
            send(f"up当前粉丝数为:{fans_num}个")
        else:
            fans_num = api.up_fans_nums(uid)
            send(f"up当前粉丝数为:{fans_num}个")

    elif message.startswith("发邮件给"):
        name = data["sender"]["nickname"]
        datas = re.findall("发邮件给(.*)标题(.*)内容(.*)", message)[0]
        result = api.send_mail(name, datas[0], datas[1], datas[2])
        send(result)

    elif message == "#跑路":
        group_id = data["group_id"]
        if user_id in group_list:
            send(f"本群{Config.CHATGPT_NAME}已经跑路了")
        else:
            group_list.append(group_id)
            send(f"本群{Config.CHATGPT_NAME}跑路了哦！别想我哦~")

    elif message == "#回来" and user_id == Config.HOST:
        group_id = data["group_id"]
        if group_id in group_list:
            group_list.remove(group_id)
            send(f"本群{Config.CHATGPT_NAME}已经回来了哦")
        else:
            send(f"本群{Config.CHATGPT_NAME}一直没有跑路哦，一直在哦!")

    elif message.startswith("查看使用量"):
        try:
            if "查看使用量" in message:
                cl = clueai.Client(Config.CHATGPT_API)
                data = cl.check_usage(finetune_user=False)
                a = data["使用量"]
                send(f"已使用{a}次调用")
        except JSONDecodeError:
            send("格式错误")

    elif message == "只听我的":
        group_id = data["group_id"]
        if user_id == Config.HOST:
            if group_id not in group_list:
                group_list.append(group_id)
                send("好的主人在这个群我只听你的")
            else:
                send("主人我已经在这个群里面跑路了哦~")
        else:
            send("你是坏人")

    elif message == "听大家的" and user_id == Config.HOST:
        group_id = data["group_id"]
        if group_id in group_list:
            group_list.remove(group_id)
            send("好欸，可以和大家一起玩了")
        else:
            send("主人,我正在和大家一起玩哦!")

    elif message.startswith("搜") and user_id == Config.HOST:
        new_message = re.findall("搜(.*)", message)[0]
        send(f"正在搜索{new_message}")
        img_file = __file__
        path_list = str(img_file).split('\\')[:-1]
        path = "\\\\".join(path_list)
        try:
            selenuims.Search(new_message)
            send(f"[CQ:image,file=file:///{path}\\{new_message}.png]")
            os.remove(f"{new_message}.png")
            send(f"[CQ:at,qq={user_id}]是否使用chatgpt进行搜索(该过程需要20秒)")
            message_id = data["message_id"]
            result = api.reply(message_id)
            if result == "可以":
                send("正在搜索中")
                result = str(plugin.GPT(new_message))
                send(result)
            else:
                send("好的")
        except SyntaxError:
            send("好像进入了不知名网站")

    elif message.startswith("chatgpt"):
        send("正在搜索中....")
        new_message = re.findall("chatgpt(.*)", message)[0]
        result = str(plugin.GPT(new_message))
        send(result)


def random_reply(message):
    if random.random() < Config.RANDOM:
        send(message)


def other_menu():
    api = API()
    data = request.get_json()
    self_id = data["self_id"]
    post_type = data["post_type"]
    if "target_id" in data:
        target_id = data["target_id"]  # 戳一戳参数就一个group_id 不一样
        if self_id == target_id:
            if "group_id" in data:
                sender_id = data["sender_id"]
                other_send_group_poke(f"[CQ:poke,qq={sender_id}]")
                result = api.abuse()
                other_send_group_poke(result)
            else:
                send("你好")
    elif post_type == "request":
        flag = data["flag"]
        sub_type = data["sub_type"]
        group_id = data["group_id"]
        api.invite_group(flag, sub_type)
        if Config.APPROVE:
            other_send_host(f"邀请类型为:{sub_type}\n群号为{group_id}\n已同意")
        else:
            other_send_host(f"邀请类型为:{sub_type}\n群号为{group_id}\n已拒绝")
