from subprocess import run
import os

from blasmodcli.controller.game.group import GameCommandGroup
from blasmodcli.utils import Message


class CD(GameCommandGroup):
    """ Opens a sub-shell inside the game's directory, to easily access the game and mods files. """

    async def handle(self) -> int:
        shell = os.getenv("SHELL")
        if shell is None or len(shell) == 0:
            Message.error("The user's $SHELL variable is empty or unset.")
        run(shell, cwd=self.game.directory)
        return 0
