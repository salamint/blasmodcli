from blasmodcli.utils import Color
from blasmodcli.utils.message import Message


class Counter:

    def __init__(self, total: int, message: str):
        self.done = 0
        self.total = total
        self.message = message

    def __str__(self) -> str:
        return f"{self.done}/{self.total}"

    @property
    def finished(self):
        return self.done == self.total

    def increment(self):
        self.done += 1

    def print(self):
        color = Color.GREEN if self.finished else Color.YELLOW
        print(end="\r")
        Message.print(color, f"{self.message}... {color.fmt(self)}", nl=False)
        if self.finished:
            print(flush=True)
