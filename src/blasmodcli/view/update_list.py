import os

from blasmodcli.model import Mod
from blasmodcli.utils import Color


class UpdateList:

    def __init__(self):
        self.strings: list[str] = []
        self.number_of_strings = 0
        self.minimum_column_width = 0

    def add(self, mod: Mod):
        string = f"{mod.name} {Color.fmt(mod.latest_version, Color.YELLOW)}"
        length = len(string)
        print(length)
        self.strings.append(string)
        if length > self.minimum_column_width:
            self.minimum_column_width = length
        self.number_of_strings += 1

    def get_number_of_columns(self) -> int:
        terminal_width = os.get_terminal_size().columns - 8
        return terminal_width // self.minimum_column_width

    def display(self):
        number_of_columns = self.get_number_of_columns()
        column = 0
        for string in self.strings:
            if column > number_of_columns:
                print("\n        ", end="")
                column = 0
            if column != 0:
                print(" ", end="")
            print(string, end="")

    def sort(self):
        self.strings.sort()
