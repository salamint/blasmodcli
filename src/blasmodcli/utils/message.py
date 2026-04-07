from enum import StrEnum
from logging import getLogger, Formatter, LogRecord, DEBUG, INFO, WARNING
from typing import TextIO

from blasmodcli.utils import Color

APP_NAME = "blasmodcli"

logger = getLogger(APP_NAME)


class ArrowStyle(StrEnum):
    THICK = "=>"
    THIN = "->"

    def fmt(self, s: object, color: 'Color'):
        return f"{color.fmt(self)} {s}"


class MessageFormatter(Formatter):

    def __init__(self):
        super().__init__()

    def format(self, record: LogRecord):
        arrow = ArrowStyle.THICK
        color = Color.RED
        if record.levelno == DEBUG:
            color = Color.MAGENTA
        elif record.levelno == INFO:
            color = Color.BLUE
            arrow = ArrowStyle.THIN
        elif record.levelno == WARNING:
            color = Color.YELLOW
            arrow = ArrowStyle.THIN
        return f"{color.fmt(arrow)} {super().format(record)}"


class Message:

    @staticmethod
    def print(color: 'Color', message: str, nl: bool = True, stream: TextIO | None = None):
        arrow = color.fmt("=>")
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
