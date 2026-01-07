#!/bin/env python3
from argparse import ArgumentParser
import sys

from blasmodcli.controller import *
from blasmodcli.games import Game
from blasmodcli.utils import Message
from blasmodcli.utils.cli import CommandLineInterface


def get_cli(game: 'Game') -> 'CommandLineInterface':
    cli = CommandLineInterface(game)

    # Game commands
    cli.add_handler(Backup)
    cli.add_handler(Configure)
    cli.add_handler(List)
    cli.add_handler(Search)
    cli.add_handler(Update)

    # Mod commands
    cli.add_handler(Activate)
    cli.add_handler(Deactivate)
    cli.add_handler(Info)
    cli.add_handler(Install)
    cli.add_handler(Uninstall)
    cli.add_handler(Upgrade)

    return cli


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument(
        "game",
        choices=tuple(Game.all.keys()),
        help="Name of the game on which to operate.",
        type=str
    )
    parser.add_argument(
        "args",
        help="Arguments to pass to the handler.",
        nargs='*'
    )

    ns = parser.parse_args()
    game = Game.all.get(ns.game)
    if game is not None:
        cli = get_cli(game)
        return cli.parse_args(ns.args)
    Message.error("No game selected")
    return 1


if __name__ == '__main__':
    sys.exit(main())
