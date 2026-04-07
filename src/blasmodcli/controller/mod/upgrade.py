from zipfile import BadZipFile, ZipFile

from blasmodcli.controller.mod.group import ModCommandGroup
from blasmodcli.exceptions import NothingToDoException
from blasmodcli.model import Installation, File
from blasmodcli.utils import Color, Message
from blasmodcli.utils.cli import Argument
from blasmodcli.view import format_mod_name, accept_or_cancel, NumberedList


def print_upgrade_list(upgrades: list[Installation]):
    Message.info(f"{len(upgrades)} new upgrades are available:")
    for installation in upgrades:
        prefix = f"  {Color.GREEN.fmt("-")}"
        current_version = Color.YELLOW.fmt(installation.version)
        newest_version = Color.YELLOW.fmt(installation.mod.latest_version)
        print(f"{prefix} {format_mod_name(installation.mod)} {current_version} -> {newest_version}")


class Upgrade(ModCommandGroup):
    """ Upgrades all mods (or the specified ones) to their latest version. """

    yes: bool = Argument("-y", default=False, help="Skip the confirmation message.")

    upgrades: list[Installation]

    def post_init(self) -> int:
        exit_code = super().post_init()
        if exit_code:
            return exit_code

        if len(self.mod_versions) == 0:
            self.mod_versions = self.fs.installations.get_upgrades(self.game)

        self.upgrades = []
        for mod_version in self.mod_versions:
            self.upgrades.append(self.fs.installations.get(mod_version))
        return 0

    def upgrade_mods(self, upgrades: list[Installation]):
        numbered_list = NumberedList(len(upgrades))
        failed = 0
        for installation in upgrades:
            progress = numbered_list.add_progress(f"Upgrading {installation.mod.display_name}...")
            try:
                self.upgrade_mod(installation)
            except BadZipFile:
                progress.failure(f"Bad ZIP file: {self.fs.cache.file(installation.mod_version)}")
                failed += 1
            else:
                progress.success()
        return failed

    def upgrade_mod(self, installation: Installation):
        files = {file.relpath: file for file in installation.files}

        with ZipFile(self.fs.cache.file(installation.mod_version), "r") as zipfile:
            for info in zipfile.infolist():
                zipfile.extract(info, self.game.modding_directory)
                file = files.get(info.filename)
                if file is None:
                    file = File(installation, relpath=info.filename)
                    installation.files.append(file)
                else:
                    file.update_hash()

        installation.persist()

    async def handle(self) -> int:
        number_of_upgrades = len(self.upgrades)
        if number_of_upgrades == 0:
            raise NothingToDoException("There is no upgrade currently available.")

        print_upgrade_list(self.upgrades)

        if not self.yes:
            accept_or_cancel(f"Are you sure you want to upgrade {number_of_upgrades} mods?")

        self.upgrade_mods(self.upgrades)
        return 0
