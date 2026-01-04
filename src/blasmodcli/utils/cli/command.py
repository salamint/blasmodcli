from abc import ABCMeta, ABC, abstractmethod
from argparse import Namespace
from typing import Any

from blasmodcli.exceptions import DoneException, CancelException
from blasmodcli.utils import Message
from blasmodcli.utils.cli.argument import Argument


class MetaCommandHandler(ABCMeta):

    def __init__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        super().__init__(name, bases, dct)
        cls.arguments: dict[str, 'Argument'] = {}

        for attr, value in dct.items():
            if isinstance(value, Argument):
                cls.arguments[attr] = value

        for arg_name, arg_type in cls.__annotations__.items():
            arg = cls.arguments[arg_name]
            arg.add_annotation(arg_name, arg_type)

    @property
    def command(cls):
        return cls.__name__.lower()

    def add_subparser_to(cls, subparsers) -> None:
        subparser = subparsers.add_parser(cls.command, help=cls.__doc__)
        for arg in cls.arguments.values():
            arg.add_argument_to(subparser)

    def call_handler(cls, namespace: Namespace) -> int:
        instance = cls(namespace)

        try:
            return instance.handle()
        except DoneException as e:
            Message.success(str(e))
            return 0
        except CancelException as e:
            Message.error(str(e))
            return 0
        except Exception as e:
            Message.error(f"{e.__class__.__name__}: {e}")
            return 1


class CommandHandler(ABC, metaclass=MetaCommandHandler):

    def __init__(self, namespace: Namespace):
        for arg in self.arguments:
            setattr(self, arg, getattr(namespace, arg))

    @abstractmethod
    def handle(self) -> int:
        raise NotImplementedError
