from blasmodcli.controller.mod.group import ModCommandGroup
from blasmodcli.exceptions import NothingToDoException
from blasmodcli.model import ModVersion
from blasmodcli.utils import Message
from blasmodcli.utils.cli import Argument
from blasmodcli.utils.jobs import Downloader
from blasmodcli.view import step, accept_or_cancel


class Download(ModCommandGroup):
    """ Downloads the given mod. By default, downloads the latest version and its dependencies. """

    force: bool = Argument("-f", default=False, help="If the mod is already cached, overwrite the previous archive.")
    not_recursive: bool = Argument("-n", default=False, help="Do not download mods that this mod depends on.")
    yes: bool = Argument("-y", default=False, help="Skip the confirmation message.")

    @step("Downloading mods...")
    async def download_mods(self):
        number_of_mods = len(self.mod_versions)
        downloader = Downloader(self.mod_versions, self.fs.cache)
        await downloader.run()
        Message.success(f"Successfully downloaded {number_of_mods} mods!")

    def filter_cached(self):
        filtered = []
        for mod, version in self.mod_versions:
            if not self.fs.cache.has(mod, version):
                filtered.append(ModVersion(mod, version))
        self.mod_versions = filtered

    async def handle(self) -> int:
        if not self.not_recursive:
            exit_code = self.resolve_dependencies()
            if exit_code:
                return exit_code

        if not self.force:
            self.filter_cached()

        if len(self.mod_versions) == 0:
            raise NothingToDoException("The mod and its dependencies are already cached.")

        self.print_mod_list("download")
        if not self.yes:
            number_of_mods = len(self.mod_versions)
            accept_or_cancel(f"Are you sure you want to download {number_of_mods} mods?")

        await self.download_mods()
        return 0
