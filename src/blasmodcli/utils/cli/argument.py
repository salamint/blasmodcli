from argparse import ArgumentParser
from typing import Any


class Argument:

    def __init__(self, *names: str, default: Any = None, type: type = None, help: str = None):
        self.names = list(names)
        self.default = default
        self.type = type
        self.help = help

    def add_argument_to(self, parser: ArgumentParser):
        parser.add_argument(
            *self.names,
            default=self.default,
            type=self.type,
            help=self.help
        )
