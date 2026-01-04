from abc import ABCMeta, ABC, abstractmethod
from typing import Any


class MetaCommandHandler(ABCMeta):

    def __init__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        super().__init__(name, bases, dct)
        cls.arguments: list['Argument'] = []
        print(name)
        for k, v in cls.__annotations__.items():
            print(k, v)

    def add_subparser_to(cls, subparsers) -> None:
        subparser = subparsers.add_parser(cls.__name__.lower(), help=cls.__doc__)
        for arg in cls.arguments:
            subparser.add_argument(*arg.names)


class CommandHandler(ABC, metaclass=MetaCommandHandler):

    @abstractmethod
    def handle(self, *args, **kwargs):
        raise NotImplementedError
