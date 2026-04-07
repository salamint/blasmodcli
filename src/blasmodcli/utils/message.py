from logging import getLogger
from typing import TextIO

from blasmodcli.utils import Color

APP_NAME = "blasmodcli"

logger = getLogger(APP_NAME)


class Message:

    @staticmethod
    def print(color: 'Color', message: str, nl: bool = True, stream: TextIO | None = None):
        arrow = Color.fmt("=>", color)
        print(f"{arrow} {message}", end="\n" if nl else "", file=stream, flush=True)

    @staticmethod
    def debug(message: str):
        return Message.print(Color.MAGENTA, message)

    @staticmethod
    def success(message: str):
        return Message.print(Color.GREEN, message)

    @staticmethod
    def info(message: str):
        return Message.print(Color.BLUE, message)

    @staticmethod
    def warning(message: str):
        return Message.print(Color.YELLOW, message)

    @staticmethod
    def error(message: str):
        return Message.print(Color.RED, message)
