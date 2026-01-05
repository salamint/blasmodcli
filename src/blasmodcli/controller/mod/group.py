from abc import ABC

from blasmodcli.model.mod import Mod
from blasmodcli.utils.cli import CommandHandler, Argument


class ModCommandGroup(CommandHandler, ABC):
    """ Regroups commands that operate on a single mod. """
    __group__ = "mod"

    mod_name: str = Argument(help="The name of the mod on which to operate.")
    mod: Mod

    def post_init(self):
        self.mod = ...
