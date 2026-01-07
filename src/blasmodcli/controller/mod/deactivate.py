from .group import ModCommandGroup

from blasmodcli.utils.cli import Argument


class Deactivate(ModCommandGroup):
    """ Removes the dynamic library file associated with the mod inside the Modding folder, thus deactivating it. """

    not_recursive: bool = Argument("-n", default=False, help="Does not deactivate mods that were only depended on by this mod.")

    def handle(self) -> int:
        raise NotImplementedError
