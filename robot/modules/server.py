import redis
from flask import Flask, request
from gevent import pywsgi
import logging
from robot.util.colorlog_format import ColoredLogger

from ..util.config import Config
from ..util.logger import Logger

app = Flask(__name__)
conn_station = []

logging.setLoggerClass(ColoredLogger)
color_log = logging.getLogger("robot")
color_log.setLevel(logging.DEBUG)


@app.route('/', methods=["POST"])
def post_data():
    from ..commands import menu
    from robot.modules.functions import API
    global conn_station
    if not conn_station:
        Logger.info("连接成功")
    conn_station = True
    data = request.get_json()
    api = API()
    if data['post_type'] == 'message':
        api.save_message()
        message = data['message']
        Logger.info(message)
        menu.menu()
    else:
        menu.other_menu()
    return "ok"


def run():
    """
    启动服务
    :return:
    """
    redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    server = pywsgi.WSGIServer(
        ('0.0.0.0', Config.RUN_AT), app)
    Logger.success("服务启动成功")
    server.serve_forever()
