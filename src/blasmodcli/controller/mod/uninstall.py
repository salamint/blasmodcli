from enum import StrEnum

from .group import ModCommandGroup

from blasmodcli.utils.cli import Argument


class UnusedDependenciesAction(StrEnum):
    NOTHING = "nothing"
    DEACTIVATE = "deactivate"
    UNINSTALL = "uninstall"


class Uninstall(ModCommandGroup):
    """ Deletes the mod and all of its files from the game's folder. """

    unused_dependencies_action: UnusedDependenciesAction = Argument(
        "--unused-deps", "-u",
        choices=[act.value for act in UnusedDependenciesAction],
        default=UnusedDependenciesAction.DEACTIVATE,
        help="The action to effectuate on all unused dependencies that were used by this mod before."
    )

    def handle(self) -> int:
        raise NotImplementedError
