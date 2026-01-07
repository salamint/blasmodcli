from .group import ModCommandGroup

from blasmodcli.utils.cli import Argument


class Activate(ModCommandGroup):
    """ Extracts the contents of the mod inside the Modding folder, thus activating it. """

    reactivate: bool = Argument("-r", default=False, help="If the mod is already activated, reactivates it. Can be used for debugging or trying to fix collision issues.")
    not_recursive: bool = Argument("-n", default=False, help="Does not activate mods that this mod depends on.")

    def handle(self) -> int:
        raise NotImplementedError
