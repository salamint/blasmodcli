from abc import ABC

from blasmodcli.utils.cli import CommandHandler


class GameCommandGroup(CommandHandler, ABC):
    """ Regroups commands that operate on a single mod. """
    __group__ = "game"
