from argparse import ArgumentParser
from typing import Dict, Sequence

from blasmodcli.config import Configuration
from blasmodcli.model.game import Game
from blasmodcli.repositories import Warehouse
from blasmodcli.utils import Directories
from blasmodcli.utils.cli.context import CommandContext
from blasmodcli.utils.cli.meta_handler import MetaCommandHandler


class CommandLineInterface:

    def __init__(self, config: Configuration, directories: Directories, warehouse: Warehouse):
        self.context = CommandContext(config, directories, warehouse)
        self.parser = ArgumentParser()
        self.subparsers = self.parser.add_subparsers(dest="handler")
        self.handlers: 'Dict[str, MetaCommandHandler]' = {}

    def add_handler(self, handler: 'MetaCommandHandler'):
        handler.add_subparser_to(self.subparsers)
        self.handlers[handler.command] = handler

    def parse_args(self, game: 'Game', args: Sequence[str] | None = None) -> int:
        namespace = self.parser.parse_args(args)
        if namespace.handler:
            handler = self.handlers[namespace.handler]
            return handler.call_handler(self.context, game, namespace)
        self.parser.print_help()
        return 0
