from blasmodcli.utils import Color
from blasmodcli.view.progress import Progress


class NumberedList:

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
