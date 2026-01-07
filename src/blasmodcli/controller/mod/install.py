from zipfile import ZipFile, BadZipFile

from blasmodcli.controller.mod.download import Download
from blasmodcli.controller.mod.group import ModCommandGroup
from blasmodcli.exceptions import NothingToDoException
from blasmodcli.model import File, Installation, ModVersion
from blasmodcli.utils import Message
from blasmodcli.utils.cli import Argument
from blasmodcli.view import step, NumberedList, accept_or_cancel


class Install(ModCommandGroup):
    """ Installs the given mod. By default, downloads the mod if it is missing, and installs dependencies as well. """

    force: bool = Argument("-f", default=False, help="Overwrite the previous installation.")
    not_recursive: bool = Argument("-n", default=False, help="Do not install mods that this mod depends on.")
    re_download: bool = Argument("-r", default=False, help="Download the mod again even if the version that needs to be installed is already in the cache.")
    yes: bool = Argument("-y", default=False, help="Skip the confirmation messages (download AND install).")

    async def download_mods(self) -> int:
        return await self.call(Download, mod_names=self.mod_names, force=self.re_download, yes=self.yes)

    def filter_installed(self):
        filtered: list[ModVersion] = []
        for mod_version in self.mod_versions:
            if not self.fs.installations.has(*mod_version):
                filtered.append(mod_version)
        self.mod_versions = filtered

    @step("Installing mods...")
    def install_mods(self) -> int:
        numbered_list = NumberedList(len(self.mod_versions))
        failed = 0
        for mod_version in self.mod_versions:
            installation = self.fs.installations.get(mod_version)
            if installation is None:
                progress = numbered_list.add_progress(f"Installing {mod_version.mod.display_name}...")
                try:
                    self.new_installation(mod_version)
                except BadZipFile:
                    progress.failure(f"Bad ZIP file: {self.fs.cache.file(mod_version)}")
                    failed += 1
                else:
                    progress.success()
            else:
                progress = numbered_list.add_progress(f"Reinstalling {mod_version.mod.display_name}...")
                try:
                    self.update_existing_installation(installation)
                except BadZipFile:
                    progress.failure(f"Bad ZIP file: {self.fs.cache.file(mod_version)}")
                    failed += 1
                else:
                    progress.success()
        return failed

    def new_installation(self, mod_version: ModVersion):
        installation = self.fs.installations.new(mod_version)
        with ZipFile(self.fs.cache.file(mod_version), "r") as zipfile:
            for info in zipfile.infolist():
                zipfile.extract(info, self.game.modding_directory)
                file = File(installation, relpath=info.filename)
                installation.files.append(file)
        installation.persist()

    def update_existing_installation(self, installation: Installation):
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
        exit_code = await self.download_mods()
        if exit_code:
            return exit_code

        if not self.not_recursive:
            exit_code = self.resolve_dependencies()
            if exit_code:
                return exit_code

        if not self.force:
            self.filter_installed()

        number_of_mods = len(self.mod_versions)
        if number_of_mods == 0:
            raise NothingToDoException("The mod and its dependencies are already installed.")

        self.print_mod_list("install")
        if not self.yes:
            accept_or_cancel(f"Are you sure you want to install {number_of_mods} mods?")

        failed = self.install_mods()
        if failed:
            Message.error(f"Failed to install {failed} mods.")
            return failed
        Message.success(f"Successfully installed {number_of_mods} mods!")
        return 0
