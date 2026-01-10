from argparse import ArgumentParser
from typing import TypeVar, Generic, Tuple


T = TypeVar('T')


class Choices(Generic[T]):

    Choice = Tuple[Tuple[str], T, str]

    def __init__(self, *choices: 'Choice', default: T = None, destination: str = None):
        self.default = default
        self.destination = destination
        self.options: tuple[Choices.Choice] = choices

    def add_arguments_to(self, parser: ArgumentParser):
        for option in self.options:
            parser.add_argument(
                *option[0],
                action="store_const",
                const=option[1],
                default=self.default,
                dest=self.destination,
                help=option[2]
            )
