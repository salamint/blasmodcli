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
        if self.type is None:
            self.type = type_

        if self.is_optional():
            self.names.insert(0, "--" + name.replace("_", "-"))
        elif len(self.names) == 0:
            self.names.append(name)

    def copy(self):
        return Argument(
            *self.names,
            action=self.action,
            default=self.default,
            type=self.type,
            help=self.help
        )

    def get_action(self) -> str:
        if self.action:
            return self.action

        if self.type is bool:
            if self.default is False:
                return "store_true"
            else:
                return "store_false"
        return "store"

    def is_optional(self):
        has_default = self.default is not None
        action_is_not_store = self.get_action() != "store"
        has_multiple_names = len(self.names) > 1
        return has_default or action_is_not_store or has_multiple_names

    def add_argument_to(self, parser: ArgumentParser):
        parser.add_argument(
            *self.names,
            action=self.get_action(),
            default=self.default,
            help=self.help
        )
