from .group import GameCommandGroup

from blasmodcli.mod import ModState
from blasmodcli.utils.cli import Choices


class List(GameCommandGroup):
    """ Shows the list of every mod available (or installed, or activated). """

    state: ModState = Choices(
        (("--installed", "-i"), ModState.INSTALLED, "List only installed mods."),
        (("--activated", "-a"), ModState.ACTIVATED, "List only activated mods."),
        default=ModState.NONE
    )

    def handle(self) -> int:
        raise NotImplementedError
