import logging
from colorama import init
from .font_colors import green


init(autoreset=True)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    'WARNING': YELLOW,
    'INFO': BLUE,
    'DEBUG': BOLD_SEQ,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class ColoredLogger(logging.Logger):
    FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)


version = "0.0.1"
TIT = f"""
██████╗ ██╗   ██╗ ██████╗  ██████╗ ██████╗  ██████╗ ████████╗
██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝ ╚████╔╝ ██║   ██║██║   ██║██████╔╝██║   ██║   ██║   
██╔═══╝   ╚██╔╝  ██║▄▄ ██║██║▄▄ ██║██╔══██╗██║   ██║   ██║   
██║        ██║   ╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝   ██║   
╚═╝        ╚═╝    ╚══▀▀═╝  ╚══▀▀═╝ ╚═════╝  ╚═════╝    ╚═╝
version:{version}                                   By:云深不知处
"""


def print_logo():
    print(f'{green(TIT)}')


print_logo()
