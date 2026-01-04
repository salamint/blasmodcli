from abc import ABCMeta, ABC, abstractmethod
from typing import Any

from .argument import Argument


class MetaCommandHandler(ABCMeta):

    def __init__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        super().__init__(name, bases, dct)
        cls.arguments: dict[str, 'Argument'] = {}

        for attr, value in dct.items():
            if isinstance(attr, Argument):
                cls.arguments[name] = value

        for arg_name, arg_type in cls.__annotations__.items():
            arg = cls.arguments[arg_name]
            arg.add_annotation(arg_name, arg_type)

    def add_subparser_to(cls, subparsers) -> None:
        subparser = subparsers.add_parser(cls.__name__.lower(), help=cls.__doc__)
        for arg in cls.arguments.values():
            arg.add_argument_to(subparser)


class CommandHandler(ABC, metaclass=MetaCommandHandler):

    @abstractmethod
    def handle(self, *args, **kwargs):
        raise NotImplementedError
