import re
from shutil import get_terminal_size

from blasmodcli.model import Mod, Version
from blasmodcli.utils import Color
from blasmodcli.utils.resolver import ModVersion
from blasmodcli.utils.message import Message

ESCAPE_SEQUENCE_REGEX = re.compile(r"(\033\[([0-9]+(;[0-9]+)?)m)")
OFFSET = 8


def escaped_length(string: str) -> int:
    return len(ESCAPE_SEQUENCE_REGEX.sub("", string))


class ModList:

    def __init__(self, message: str):
        self.message = message
        self.strings: list[str] = []
        self.number_of_strings = 0
        self.minimum_column_width = 0

    def add_mod(self, mod: Mod, version: Version | None = None):
        version = version if version is not None else mod.latest_version
        mod_name = Color.fmt(mod.name, Color.BLUE if mod.is_library else Color.WHITE)
        self.add_string(f"{mod_name}-{Color.fmt(version, Color.YELLOW)}")

    def add_mods(self, mod_versions: list[ModVersion]):
        for mod, version in mod_versions:
            self.add_mod(mod, version)

    def add_string(self, string: str):
        length = escaped_length(string)
        self.strings.append(string)
        if length > self.minimum_column_width:
            self.minimum_column_width = length
        self.number_of_strings += 1

    @property
    def number_of_columns(self) -> int:
        return self.total_width // self.minimum_column_width

    @property
    def total_width(self) -> int:
        return get_terminal_size().columns - OFFSET

    def display(self):
        Message.info(self.message)
        column = 0
        for string in self.strings:
            if column == self.number_of_columns:
                print()
                column = 0

            if column == 0:
                print(" " * OFFSET, end="")
            else:
                print(end=" ")
            padding = self.minimum_column_width - escaped_length(string)
            print(string, end=" " * padding)
            column += 1
        print()

    def sort(self):
        self.strings.sort()
