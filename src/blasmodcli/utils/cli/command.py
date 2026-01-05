from abc import ABCMeta, ABC, abstractmethod
from argparse import Namespace
from typing import Any

from blasmodcli.exceptions import DoneException, CancelException
from blasmodcli.utils import Message
from blasmodcli.utils.cli.argument import Argument

_command_groups: dict[str, 'MetaCommandHandler'] = {}


class CommandLogicError(Exception):

    @classmethod
    def multiple_groups(cls, command: str, base_groups: tuple[type]):
        number_of_groups = 0
        for group in base_groups:
            if group in _command_groups.keys():
                number_of_groups += 1
        return f"The '{command}' command cannot be part of {number_of_groups} groups. it can only be in one group."


class MetaCommandHandler(ABCMeta):

    def __new__(metacls, name: str, bases: tuple[type], dct: dict[str, Any]):
        if "__group__" in dct.keys():
            group_instance = super().__new__(metacls, name, bases, dct)
            _command_groups[name] = group_instance
            return group_instance

        group = None
        for base in bases:
            group_match = _command_groups.get(base.__name__)
            if group_match is not None:
                if group is not None:
                    return CommandLogicError.multiple_groups(name, bases)
                group = group_match

        if group:
            grp_annotations = group.__annotations__.copy()
            grp_annotations.update(dct.get("__annotations__", {}))
            dct["__annotations__"] = grp_annotations

            for arg_name, arg_value in group.arguments.items():
                if arg_name not in dct.keys():
                    dct[arg_name] = arg_value.copy()
        instance = super().__new__(metacls, name, bases, dct)
        return instance

    def __init__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        super().__init__(name, bases, dct)
        cls.arguments: dict[str, 'Argument'] = {}

        for attr, value in dct.items():
            if isinstance(value, Argument):
                cls.arguments[attr] = value

        print(cls.__annotations__)
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
