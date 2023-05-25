import random


class Style(int):
    """
    样式类
    """
    Default: None = 0
    HighLight: None = 1
    UnderLine: None = 4
    Flash: None = 5
    AntiWhite: None = 7
    Invisible: None = 8


class ColorType(int):
    """
    颜色类
    """
    BLACK: None = 30
    RED: None = 31
    GREEN: None = 32
    YELLOW: None = 33
    BLUE: None = 34
    PURPLE: None = 35
    CYAN: None = 36
    WHITE: None = 37

    @classmethod
    def random(cls):
        """
        - 返回一个随机的颜色
        """
        color = [
            ColorType.BLACK,
            ColorType.RED,
            ColorType.GREEN,
            ColorType.YELLOW,
            ColorType.BLACK,
            ColorType.PURPLE,
            ColorType.CYAN,
            ColorType.WHITE
        ]
        return random.choice(color)


def __color(
        content: str,
        color: ColorType = 0,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    -color：颜色
    -style：显示的样式
    -is_back：是否为背景色
    """
    if 30 <= back <= 37 or back == 0:
        back = back + 10
        return f'\033[{style};{color};{back}m{content}\033[0m'
    else:
        raise ValueError('back的值不在定义的范围内')


def black(
        content: str,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    返回黑色字符串
    """
    formatter = __color(
        content=content,
        color=ColorType.BLACK,
        back=back,
        style=style
    )
    return formatter


def red(
        content: str,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    返回红色字符串
    """
    formatter = __color(
        content=content,
        color=ColorType.RED,
        back=back,
        style=style
    )
    return formatter


def green(
        content: str,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    返回绿色字符串
    """
    formatter = __color(
        content=content,
        color=ColorType.GREEN,
        back=back,
        style=style
    )
    return formatter


def yellow(
        content: str,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    返回黄色字符串
    """
    formatter = __color(
        content=content,
        color=ColorType.YELLOW,
        back=back,
        style=style
    )
    return formatter


def blue(
        content: str,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    返回蓝色字符串
    """
    formatter = __color(
        content=content,
        color=ColorType.BLUE,
        back=back,
        style=style
    )
    return formatter


def purple(
        content: str,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    返回紫色字符串
    """
    formatter = __color(
        content=content,
        color=ColorType.PURPLE,
        back=back,
        style=style
    )
    return formatter


def cyan(
        content: str,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    返回青色字符串
    """
    formatter = __color(
        content=content,
        color=ColorType.CYAN,
        back=back,
        style=style
    )
    return formatter


def white(
        content: str,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    返回白色字符串
    """
    formatter = __color(
        content=content,
        color=ColorType.WHITE,
        back=back,
        style=style
    )
    return formatter


def random_color(
        content: str,
        back: ColorType = 0,
        style: Style = Style.Default
) -> str:
    """
    返回随机颜色的字符串
    """
    formatter = __color(
        content=content,
        color=ColorType.random(),
        back=back,
        style=style
    )
    return formatter
