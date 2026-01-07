from abc import ABCMeta, ABC, abstractmethod
from typing import Any

from .argument import Argument


class MetaCommandHandler(ABCMeta):

    def __init__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        super().__init__(name, bases, dct)
        cls.arguments: list['Argument'] = []
        for attr in dct.values():
            if isinstance(attr, Argument):
                cls.arguments.append(attr)
        for k, v in cls.__annotations__.items():
            arg = dct[k]
            arg.names.insert(0, "--" + k.replace("_", "-"))
            arg.type = v

    def add_subparser_to(cls, subparsers) -> None:
        subparser = subparsers.add_parser(cls.__name__.lower(), help=cls.__doc__)
        for arg in cls.arguments:
            arg.add_argument_to(subparser)


class CommandHandler(ABC, metaclass=MetaCommandHandler):

    @abstractmethod
    def handle(self, *args, **kwargs):
        raise NotImplementedError
