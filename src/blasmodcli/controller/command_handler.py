from argparse import ArgumentParser
from typing import Any


class CommandLogicError(Exception):

    @classmethod
    def multiple_groups(cls, name: str, groups: list[type]):
        groups_string = ", ".join(group.__name__ for group in groups)
        return cls(f"The {CommandHandler.__name__} class {name} cannot be in multiple {CommandGroup.__name__}s: {groups_string}")


class MetaCommandHandler(type):

    _command_handlers: dict[str, 'MetaCommandHandler'] = {}
    _groups: dict[str, list['MetaCommandHandler']] = {}

    def __new__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        if len(bases) == 0:
            return super().__new__(cls, name, bases, dct)
        if CommandGroup in bases:
            cls._groups[name] = []
            return super().__new__(cls, name, bases, dct)

        groups = []
        for base in bases:
            if base.__name__ in cls._groups.keys():
                groups.append(base)

        if len(groups) == 1:
            group = groups[0]

            temp = dct.copy()
            dct = group.__dict__.copy()
            dct.update(temp)

            temp = dct["__annotations__"].copy()
            dct["__annotations__"] = group.__annotations__.copy()
            dct["__annotations__"].update(temp)
        elif len(groups) > 1:
            raise CommandLogicError.multiple_groups(name, groups)

        name = name.lower()
        instance = super().__new__(cls, name, bases, dct)
        cls._command_handlers[name] = instance
        return instance

    def __init__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        super().__init__(name, bases, dct)
        cls.group = dct.get("__group__")
        print(name, cls.group)

    @classmethod
    def add_subparsers(cls, parser: 'ArgumentParser'):
        subparsers = parser.add_subparsers(dest="handler")
        for command_handler in cls._command_handlers.values():
            command_handler.add_subparser_to(subparsers)

    def add_subparser_to(cls, subparsers) -> None:
        subparsers.add_parser(cls.__name__.lower(), help=cls.__doc__)


class CommandHandler(metaclass=MetaCommandHandler):
    pass


class CommandGroup(metaclass=MetaCommandHandler):
    pass
