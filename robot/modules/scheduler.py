import datetime

import requests
from threading import Timer

from robot.message.api import other_send_host, other_send_group
from robot.util.logger import Logger
from robot.util.config import Config


def time_printer():
    curr_time = datetime.datetime.now()
    timestamp = curr_time.hour
    time_min = curr_time.minute
    time_second = curr_time.second
    times = f"{timestamp}:{time_min}:{time_second}"
    if times == "12:0:0":
        other_send_host(f"中午啦，吃午饭了吗？注意开支哦")
    elif times == "5:0:0":
        other_send_group(f"[CQ:at,qq={Config.MONITOR}]早点休息哦！")
    elif times == "7:0:0":
        other_send_host("早上好主人")
        url = "https://xiaoapi.cn/API/zs_xw.php?num=20"
        resp = requests.get(url)
        msg = resp.json()["msg"]
        other_send_host(msg)
        other_send_group("今日新闻\n" + msg)
    loop_monitor()


def loop_monitor():
    t = Timer(1, time_printer)
    t.start()


def start():
    """
    启动定时任务
    :return:
    """
    try:
        loop_monitor()
        Logger.info("定时任务启动完成")
    except Exception as e:
        Logger.error(f'启动定时任务失败！{e}')
