import sys
from dataclasses import dataclass
from typing import TextIO

from blasmodcli.utils import Color
from blasmodcli.version import Version


class Counter:

    def __init__(self, total: int):
        self.counter = 1
        self.total = total

    def get_prefix(self):
        return Color.fmt(f"[{self.counter}/{self.total}]", Color.GREEN)

    def add_item(self, message: str):
        print(f"{self.get_prefix()} {message}")
        self.increment()

    def add_progress(self, message: str) -> 'Progress':
        print(f"{self.get_prefix()} {message}", end="", flush=True)
        self.increment()
        return Progress()

    def increment(self):
        self.counter += 1


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


class Progress:

    def __init__(self):
        self.__status = None

    def status(self, status: str, color: 'Color'):
        if self.__status is not None:
            return
        print(f" {Color.fmt(status, color)}", flush=True)
        self.__status = status

    def bool(self, boolean: bool):
        if boolean:
            self.success()
        else:
            self.failure()

    def failure(self):
        self.status("FAILURE", Color.RED)

    def success(self):
        self.status("SUCCESS", Color.GREEN)

    def version(self, version: 'Version'):
        self.status(str(version), Color.YELLOW)

    def has_succeeded(self) -> bool:
        return self.__status is not None and self.__status


class Table:

    @dataclass
    class Row:
        header: str
        value: str
        color: Color | None

        def print(self, row_size: int):
            formatted_header = Color.fmt(self.header, Color.WHITE)
            if len(self.header) < row_size:
                formatted_header += " " * (row_size - len(self.header))
            formatted_value = self.value if self.color is None else Color.fmt(self.value, self.color)
            print(formatted_header, formatted_value)

    def __init__(self, row_size: int = 0):
        self.row_size = row_size
        self.dynamic = row_size <= 0
        self.rows: list[Table.Row] = []

    def add_row(self, header: str, value, color: Color | None = None):
        header_size = len(header)
        if self.dynamic and self.row_size < header_size:
            self.row_size = header_size
        self.rows.append(Table.Row(header, value, color))

    def print(self):
        for row in self.rows:
            row.print(self.row_size)
