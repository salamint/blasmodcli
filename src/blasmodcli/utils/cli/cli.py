from argparse import ArgumentParser
from typing import Callable, Dict, Sequence, Union

from blasmodcli.games import Game
from blasmodcli.utils.cli.command import MetaCommandHandler

Handler = Union[Callable[[], int], Callable[[...], int]]


class CommandLineInterface:

    def __init__(self, game: 'Game'):
        self.game = game
        self.parser = ArgumentParser(self.game.tool_name)
        self.subparsers = self.parser.add_subparsers(dest="handler")
        self.handlers: 'Dict[str, MetaCommandHandler]' = {}

    def add_handler(self, handler: 'MetaCommandHandler'):
        handler.add_subparser_to(self.subparsers)
        self.handlers[handler.command] = handler

    def parse_args(self, args: Sequence[str] | None = None) -> int:
        ns = self.parser.parse_args(args)
        if ns.handler:
            return self.handlers[ns.handler].call_handler(ns)
        self.parser.print_help()
        return 0
