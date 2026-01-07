from pathlib import Path

from .group import GameCommandGroup

from blasmodcli.utils.cli import Argument


class Backup(GameCommandGroup):
    """ Backs up your saves into an archive and exports them. """

    destination: Path = Argument("-d", default=Path.cwd(), help="The name of the archive, destination directory or the complete path to the destination archive.")

    def handle(self) -> int:
        raise NotImplementedError
