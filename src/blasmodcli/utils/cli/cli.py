from argparse import ArgumentParser
from typing import Callable, Dict, Sequence, Union

from blasmodcli.model.game import Game
from blasmodcli.utils.cli.command import MetaCommandHandler

Handler = Union[Callable[[], int], Callable[[...], int]]


class CommandLineInterface:

    def __init__(self):
        self.parser = ArgumentParser()
        self.subparsers = self.parser.add_subparsers(dest="handler")
        self.handlers: 'Dict[str, MetaCommandHandler]' = {}

    def add_handler(self, handler: 'MetaCommandHandler'):
        handler.add_subparser_to(self.subparsers)
        self.handlers[handler.command] = handler

    def parse_args(self, game: 'Game', args: Sequence[str] | None = None) -> int:
        namespace = self.parser.parse_args(args)
        if namespace.handler:
            return self.handlers[namespace.handler].call_handler(game, namespace)
        self.parser.print_help()
        return 0
