from robot.modules import scheduler
from robot.util import config
from robot.util.logger import Logger
from robot.modules import server

if __name__ == '__main__':
    config.load()  # 加载配置
    scheduler.start()  # 启动定时任务
    server.run()  # 启动flask与redis服务
