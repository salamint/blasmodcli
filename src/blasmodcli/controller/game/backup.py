from datetime import datetime
from pathlib import Path
from shutil import make_archive

from blasmodcli.controller.game.group import GameCommandGroup
from blasmodcli.utils import Message
from blasmodcli.utils.cli import Argument

BACKUP_DATETIME_FORMAT = "%Y-%m-%d_%Hh%Mm%Ss"


class Backup(GameCommandGroup):
    """ Backs up your saves into an archive and exports them. """

    destination: Path = Argument("-d", default=Path.cwd(), help="The name of the archive, destination directory or the complete path to the destination archive.")

    def get_final_destination(self):
        if self.destination.is_dir():
            return self.destination / f"BlasphemousSavesBackup_{datetime.now().strftime(BACKUP_DATETIME_FORMAT)}"
        elif self.destination.suffix == ".zip":
            return self.destination.with_suffix("")
        return self.destination

    def handle(self) -> int:
        Message.info("Backing up saves data...")
        destination = self.get_final_destination()

        make_archive(str(self.destination), "zip", self.game.saves_directory)
        Message.success(f"Saves data backed up at '{destination}'!")
        return 0
