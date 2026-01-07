from blasmodcli.controller.game.group import GameCommandGroup
from blasmodcli.model import ModState
from blasmodcli.utils.cli import Choices
from blasmodcli.view import Formatter


class List(GameCommandGroup):
    """ Shows the list of every mod available (or installed, or activated). """

    state: ModState = Choices(
        (("--installed", "-i"), ModState.INSTALLED, "List only installed mods."),
        (("--cached", "-c"), ModState.CACHED, "List only activated mods."),
        default=ModState.NONE
    )

    @property
    def is_local(self):
        return self.state >= ModState.INSTALLED

    async def handle(self) -> int:
        formatter = Formatter(self.fs, self.state)
        for mod, version in self.get_mods(self.state):
            formatter.summary(mod, version)
        return 0
