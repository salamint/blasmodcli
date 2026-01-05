from argparse import ArgumentParser
from typing import Any


class Argument:

    def __init__(self, *names: str, action: str = None, default: Any = None, help: str = None, type: type = None):
        self.names = list(names)
        self.action = action
        self.default = default
        self.help = help
        self.type = type

    def add_annotation(self, name: str, type_: type):
        self.names.insert(0, "--" + name.replace("_", "-"))
        if self.type is None:
            self.type = type_

    def copy(self):
        return Argument(
            *self.names,
            action=self.action,
            default=self.default,
            type=self.type,
            help=self.help
        )

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
