import yaml

from robot.util.logger import Logger


class Config(object):
    HOST: int
    PORT: str
    BOT_NAME: str
    OTHER_INFO: str
    MONITOR: int
    MONITOR_GROUP: int
    CHATGPT_NAME: str
    CHATGPT_API: str
    RANDOM: float
    APPROVE: bool

    RUN_AT: str


def load():
    """
    加载配置
    :return:
    """
    with open("data.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    with open("qq_login/config.yml", "r", encoding="utf-8") as f:
        url = yaml.safe_load(f)
    Config.HOST = config["initialization"]["host"]
    Config.PORT = config["initialization"]["port"]
    Config.MONITOR = config["initialization"]["monitor"]
    Config.BOT_NAME = config["initialization"]["robot_name"]
    Config.OTHER_INFO = config["other_information"]["menu"]
    Config.CHATGPT_NAME = config["initialization"]["chatgpt_name"]
    Config.RANDOM = config["initialization"]["robot_answer"]
    Config.CHATGPT_API = config["initialization"]["chatgpt_api"]
    Config.APPROVE = config["initialization"]["approve"]
    Config.MONITOR_GROUP = config["initialization"]["monitor_group"]
    Config.RUN_AT = int(url["servers"][0]["http"]["post"][-1]["url"].split(":")[-1].replace("/", ""))
    Logger.success('Config loaded successful')
