from abc import ABC
from argparse import Namespace

from blasmodcli.utils.cli import CommandHandler, Argument


class ModCommandGroup(CommandHandler, ABC):
    """ Regroups commands that operate on a single mod. """
    __group__ = "mod"

    mod_name: str = Argument(help="The name of the mod on which to operate.")

    def __init__(self, namespace: Namespace):
        super().__init__(namespace)
        # TODO: Add the mod attribute
