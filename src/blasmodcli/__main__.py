#!/bin/env python3
from argparse import ArgumentParser
import sys

from blasmodcli.cli import CommandLineInterface
from blasmodcli.games import Game
from blasmodcli.utils import Message


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
        cli = CommandLineInterface(game)
        cli.add_all_handlers()
        return cli.parse_args(ns.args)
    Message.error("No game selected")
    return 1


if __name__ == '__main__':
    sys.exit(main())
