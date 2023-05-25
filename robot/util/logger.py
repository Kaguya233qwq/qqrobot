from datetime import datetime

from colorama import init

from .font_colors import (
    Style, white, yellow, blue,
    red, purple, green, cyan
)

init(autoreset=True)


class LoggerLevel(object):
    DEBUG = 0
    SUCCESS = 1
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4
    SYSTEM = 5  # 最高优先级，不受当前日志等级限制


LEVEL = LoggerLevel.INFO


def set_level(level: LoggerLevel) -> None:
    """
    设置日志等级
    """
    global LEVEL
    LEVEL = level


class Logger(object):
    """日志类"""

    @classmethod
    def debug(cls, message):
        """
        输出成功信息

        :param message: 成功信息
        """
        results = cls.__color_formatter(
            level=white(
                'SUCCESS',
                style=Style.HighLight
            ),
            content=message)
        if LEVEL == 0:
            print(results)

    @classmethod
    def success(cls, message) -> None:
        """
        输出成功信息

        :param message: 成功信息
        """
        results = cls.__color_formatter(
            level=green(
                'SUCCESS',
                style=Style.HighLight
            ),
            content=message)
        if LEVEL <= 1:
            print(results)

    @classmethod
    def info(cls, message) -> None:
        """
        输出程序运行详细信息

        :param message: 详细信息
        """
        results = cls.__color_formatter(
            level=blue(
                'INFO',
                style=Style.HighLight
            ),
            content=message)
        if LEVEL <= 1:
            print(results)

    @classmethod
    def warning(cls, message) -> None:
        """
        输出程序运行警告信息

        :param message: 警告信息
        :return:
        """
        results = cls.__color_formatter(
            level=yellow(
                'WARNING',
                style=Style.HighLight
            ),
            content=message)
        if LEVEL <= 2:
            print(results)

    @classmethod
    def error(cls, message) -> None:
        """
        输出程序运行错误信息

        :param message: 错误信息
        :return:
        """
        results = cls.__color_formatter(
            level=red(
                'ERROR',
                style=Style.HighLight
            ),
            content=message)
        if LEVEL <= 3:
            print(results)

    @classmethod
    def fatal(cls, message) -> None:
        """
        输出程序运行严重错误信息

        :param message: 严重错误信息
        :return:
        """
        results = cls.__color_formatter(
            level=purple(
                'FATAL',
                style=Style.HighLight
            ),
            content=message)
        if LEVEL <= 4:
            print(results)

    @classmethod
    def system(cls, message) -> None:
        """
        输出程序系统级别信息，不受日志等级约束

        :param message: 系统级别信息
        :return:
        """
        results = cls.__color_formatter(
            level=cyan(
                'SYSTEM',
                style=Style.HighLight
            ),
            content=message)
        print(results)

    @classmethod
    def __color_formatter(
            cls,
            level: str,
            content: str
    ) -> str:
        """
        -level：日志等级
        -content：要格式化的内容内容
        """
        times = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatter = f'{white(times)}-[{level}] {content}'
        return formatter
