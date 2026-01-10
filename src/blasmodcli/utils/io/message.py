from typing import TextIO

from blasmodcli.utils import Color
from blasmodcli.utils.io.progress import Progress


class Message:

    @staticmethod
    def print(color: 'Color', message: str, nl: bool = True, stream: TextIO | None = None):
        arrow = Color.fmt("=>", color)
        print(f"{arrow} {message}", end="\n" if nl else "", file=stream, flush=True)

    @staticmethod
    def ask(message: str, default: bool = False) -> bool:
        Message.print(Color.YELLOW, message, nl=False)
        if default:
            answer = input(" [Y/n] ")
            return len(answer) == 0 or answer.lower() == "y"
        else:
            answer = input(" [y/N] ")
            return answer.lower() == "y"

    @staticmethod
    def progress(message: str):
        Message.print(Color.YELLOW, f"{message}...", nl=False)
        return Progress()

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
