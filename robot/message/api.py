import requests
from flask import request

from ..util.config import Config


def send(message):
    """
    发送消息不分信息类型
    """
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
    url = f"{Config.PORT}/send_msg"
    requests.get(url, params=params)


def other_send_group(message):
    """
    发送群聊信息
    """
    group_id = Config.MONITOR_GROUP
    params = {
        "auto_escape": False,
        "message": message,
        "group_id": group_id
    }
    url = f"{Config.PORT}/send_group_msg"
    requests.get(url, params=params)


def other_send_private(message, group_id=None):
    """
    发送私聊信息，不支持临时会话
    """
    data = request.get_json()
    user_id = data["user_id"]
    params = {
        "auto_escape": False,
        "message": message,
        "user_id": user_id,
        "group_id": group_id
    }
    url = f"{Config.PORT}/send_private_msg"
    requests.get(url, params=params)


def other_send_host(message):
    """
    发送消息给机器人主人
    """
    params = {
        "auto_escape": False,
        "message": message,
        "user_id": Config.HOST
    }
    url = f"{Config.PORT}/send_private_msg"
    requests.get(url, params=params)


def other_send_group_poke(message):
    """
    发送戳一戳信息,需要传入信息，当用户戳机器人时发送信息
    """
    data = request.get_json()
    group_id = data["group_id"]
    params = {
        "auto_escape": False,
        "message": message,
        "group_id": group_id
    }
    url = f"{Config.PORT}/send_group_msg"
    requests.get(url, params=params)
