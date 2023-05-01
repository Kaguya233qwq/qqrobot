import os
import random
import re
import selenuims
from flask import request
from main import API, config, approve
import psutil
import platform
import plugin
from clueai.error import ClueaiError

host = config["initialization"]["host"]
monitor = config["initialization"]["monitor"]
robot_name = config["initialization"]["robot_name"]
other_information = config["other_information"]["menu"]
chatgpt_name = config["initialization"]["chatgpt_name"]
random_randon = config["initialization"]["robot_answer"]
api = API()
temp = []
host_temp = [host]
group_list = []


def menu():
    data = request.get_json()
    message = data['message']
    message_type = data["message_type"]
    user_id = data["user_id"]
    self_id = data["self_id"]
    random_reply(message)
    if message == robot_name:
        result = api.abuse()
        api.send(result)

    elif message.startswith(robot_name):
        group_id = data["group_id"]
        if str(user_id) in temp:
            api.send("你好像被加入黑名单了你想想你干了什么")
        elif "机器人" in message:
            api.send(f"我是真人，这年头谁用机器人啊\n{other_information}")
        elif message.startswith(f"{robot_name}查看视频评论"):
            oid = str(re.findall(f"{robot_name}查看视频评论(.*)", message)[0])
            content = api.bilbil_content(oid)
            api.send("\n".join(content))
        elif "检查系统" in message:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
            mem = psutil.virtual_memory()
            mem_usage = mem.percent
            disk_usage = psutil.disk_usage("/")
            api.send(
                f'当前cup使用率为:{cpu_percent}%\n当前cpu占用为详情为'
                f'\n{cpu_percents}\nRAM占用率为:{mem_usage}%\n磁盘占用率:{disk_usage.percent}%')
            api.send(f"操作系统及版本信息{platform.platform()}\n获取系统版本号{platform.version()}"
                     f"\n获取系统名称{platform.system()}\n处理器类型{platform.processor()}")
        elif group_id not in group_list:
            new_message = str(re.findall(f"{robot_name}(.*)", message)[0])
            result = api.free_gpt(new_message)
            api.send(result)

    elif message_type == "private":
        result = api.free_gpt(message)
        api.send(result)

    elif f"[CQ:at,qq={self_id}]" in message and str(user_id) not in temp:
        new_message = message.replace(f"[CQ:at,qq={self_id}]", "")
        group_id = data["group_id"]
        if str(user_id) in temp:
            api.send("你好像被加入黑名单了你想想你干了什么")
        elif "机器人" in message:
            api.send("我是真人，我只是模仿机器人")
        elif "视频" in message:
            api.send("视频需要时间请勿重复发送")
            girl_url = api.girl_url()
            api.send(f"[CQ:video,file=http:{girl_url}]")
        elif group_id not in group_list:
            try:
                result = api.free_gpt(new_message)
                api.send(result)
            except ClueaiError:
                api.send("你他妈的")

    elif message.startswith(robot_name) and str(user_id) not in temp:
        new_message = message.replace(robot_name, "")
        result = api.free_gpt(new_message)
        api.send(result)

    elif random.random() < random_randon:
        if "为什么" in message:
            result = api.free_gpt(message)
            api.send(result)

    elif message.startswith("up粉丝数"):
        uid = str(re.findall("up粉丝数(.*)", message)[0])
        if uid == "":
            fans_num = api.up_fans_nums()
            api.send(f"up当前粉丝数为:{fans_num}个")
        else:
            fans_num = api.up_fans_nums(uid)
            api.send(f"up当前粉丝数为:{fans_num}个")

    elif message.startswith("发邮件给"):
        name = data["sender"]["nickname"]
        datas = re.findall("发邮件给(.*)标题(.*)内容(.*)", message)[0]
        result = api.send_mail(name, datas[0], datas[1], datas[2])
        api.send(result)

    elif message == "#跑路":
        group_id = data["group_id"]
        if user_id in group_list:
            api.send(f"本群{chatgpt_name}已经跑路了")
        else:
            group_list.append(group_id)
            api.send(f"本群{chatgpt_name}跑路了哦！别想我哦~")

    elif message == "#回来" and user_id == host:
        group_id = data["group_id"]
        if group_id in group_list:
            group_list.remove(group_id)
            api.send(f"本群{chatgpt_name}已经回来了哦")
        else:
            api.send(f"本群{chatgpt_name}一直没有跑路哦，一直在哦!")

    elif message == "只听我的":
        group_id = data["group_id"]
        if user_id == host:
            if group_id not in group_list:
                group_list.append(group_id)
                api.send("好的主人在这个群我只听你的")
            else:
                api.send("主人我已经在这个群里面跑路了哦~")
        else:
            api.send("你是坏人")

    elif message == "听大家的" and user_id == host:
        group_id = data["group_id"]
        if group_id in group_list:
            group_list.remove(group_id)
            api.send("好欸，可以和大家一起玩了")
        else:
            api.send("主人,我正在和大家一起玩哦!")

    elif message.startswith("搜索") and user_id == host:
        new_message = re.findall("搜索(.*)", message)[0]
        api.send(f"正在搜索{new_message}")
        img_file = __file__
        path_list = str(img_file).split('\\')[:-1]
        path = "\\\\".join(path_list)
        try:
            selenuims.Search(new_message)
            api.send(f"[CQ:image,file=file:///{path}\\{new_message}.png]")
            os.remove(f"{new_message}.png")
            api.send(f"[CQ:at,qq={user_id}]是否使用chatgpt进行搜索(该过程需要20秒)")
            message_id = data["message_id"]
            result = api.reply(message_id)
            if result == "可以":
                api.send("正在搜索中")
                result = str(plugin.GPT(new_message))
                api.send(result)
            else:
                api.send("好的")
        except SyntaxError:
            api.send("好像进入了不知名网站")

    elif message.startswith("chatgpt"):
        api.send("正在搜索中....")
        new_message = re.findall("chatgpt(.*)", message)[0]
        result = str(plugin.GPT(new_message))
        api.send(result)


def random_reply(message):
    if random.random() < random_randon:
        api.send(message)


def other_menu():
    data = request.get_json()
    self_id = data["self_id"]
    post_type = data["post_type"]
    if "target_id" in data:
        target_id = data["target_id"]  # 戳一戳参数就一个group_id 不一样
        if self_id == target_id:
            if "group_id" in data:
                sender_id = data["sender_id"]
                api.other_send_group_poke(f"[CQ:poke,qq={sender_id}]")
                result = api.abuse()
                api.other_send_group_poke(result)
            else:
                api.send("你好")
    elif post_type == "request":
        flag = data["flag"]
        sub_type = data["sub_type"]
        group_id = data["group_id"]
        api.invite_group(flag, sub_type)
        if approve:
            api.other_send_host(f"邀请类型为:{sub_type}\n群号为{group_id}\n已同意")
        else:
            api.other_send_host(f"邀请类型为:{sub_type}\n群号为{group_id}\n已拒绝")
