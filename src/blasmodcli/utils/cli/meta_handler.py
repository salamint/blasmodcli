import asyncio
from abc import ABCMeta
from argparse import Namespace
from typing import Any, Self

from blasmodcli.exceptions import NothingToDoException, UserCancelException, CommandInMultipleGroupsError
from blasmodcli.model import Game
from blasmodcli.utils.cli.argument import Argument
from blasmodcli.utils.cli.choices import Choices
from blasmodcli.utils.cli.context import CommandContext
from blasmodcli.view import Message

Attributes = dict[str, Any]


class MetaCommandHandler(ABCMeta):

    _command_groups: dict[str, 'MetaCommandHandler'] = {}

    @classmethod
    def get_group(metacls, name: str, bases: tuple[type]) -> Self | None:
        in_group = None
        for group_name, group in metacls._command_groups.items():
            if group_name not in bases:
                continue
            if in_group is not None:
                group_names = list(metacls._command_groups.keys())
                raise CommandInMultipleGroupsError(group_names, name, bases)
            in_group = group
        return in_group

    def __new__(metacls, name: str, bases: tuple[type], dct: Attributes):
        if "__group__" in dct.keys():
            group_instance = super().__new__(metacls, name, bases, dct)
            metacls._command_groups[name] = group_instance
            return group_instance

        group = metacls.get_group(name, bases)
        if group is not None:
            inherit_from_group(dct, group)

        instance = super().__new__(metacls, name, bases, dct)
        return instance

    def __init__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        super().__init__(name, bases, dct)
        cls.arguments: dict[str, 'Argument'] = {}
        cls.choices: dict[str, 'Choices'] = {}

        for attr, value in dct.items():
            if isinstance(value, Argument):
                cls.arguments[attr] = value
            elif isinstance(value, Choices):
                cls.choices[attr] = value

        cls.add_annotations()

    @property
    def command(cls):
        return cls.__name__.lower()

    def add_annotations(cls):
        for arg_name, arg_type in cls.__annotations__.items():
            arg = cls.arguments.get(arg_name)
            choices = cls.choices.get(arg_name)
            if arg is not None:
                arg.add_annotation(arg_name, arg_type)
            elif choices is not None:
                choices.destination = arg_name

    def add_subparser_to(cls, subparsers) -> None:
        subparser = subparsers.add_parser(cls.command, help=cls.__doc__)
        for arg in cls.arguments.values():
            arg.add_argument_to(subparser)
        for arg in cls.choices.values():
            arg.add_arguments_to(subparser)

    def call_handler(cls, context: CommandContext, game: Game, namespace: Namespace) -> int:
        instance = cls(context, game, namespace)

        try:
            exit_code = instance.post_init()
            if exit_code:
                return exit_code
            return asyncio.run(instance.handle())
        except NothingToDoException as e:
            Message.success(str(e))
            return 0
        except UserCancelException as e:
            Message.error(str(e))
            return 0
        except Exception as e:
            Message.error(f"{e.__class__.__name__}: {e}")
            raise e


def inherit_from_group(dct: Attributes, group: MetaCommandHandler):
    grp_annotations = group.__annotations__.copy()
    grp_annotations.update(dct.get("__annotations__", {}))
    dct["__annotations__"] = grp_annotations

    for arg_name, arg_value in group.arguments.items():
        if arg_name not in dct.keys():
            dct[arg_name] = arg_value.copy()
