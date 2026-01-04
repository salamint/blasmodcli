from argparse import ArgumentParser
from typing import Any


class Argument:

    def __init__(self, *names: str, action: str = None, default: Any = None, type: type = None, help: str = None):
        self.action = action
        self.names = list(names)
        self.default = default
        self.type = type
        self.help = help

    def add_annotation(self, name: str, type_: type):
        self.names.insert(0, "--" + name.replace("_", "-"))
        if self.type is None:
            self.type = type_

    def get_action(self) -> str | None:
        if self.action:
            return self.action

        if self.type is bool:
            if self.default is False:
                return "store_true"
            else:
                return "store_false"
        return None

    def add_argument_to(self, parser: ArgumentParser):
        parser.add_argument(
            *self.names,
            action=self.get_action(),
            default=self.default,
            help=self.help
        )
