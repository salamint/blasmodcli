from .group import ModCommandGroup

from blasmodcli.utils.cli import Argument


class Install(ModCommandGroup):
    """ Downloads a mod and does not activate it immediately. """

    force: bool = Argument("-f", default=False, help="If the mod is already installed, overwrites the previous installation.")
    do_not_activate: bool = Argument("-d", default=False, help="Whether to activate the mod and its dependencies after the installation or not.")
    not_recursive: bool = Argument("-n", default=False, help="Does not install mods that this mod depends on.")

    def handle(self) -> int:
        raise NotImplementedError
