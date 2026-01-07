from pathlib import Path
from shutil import which
from subprocess import run
from zipfile import ZipFile

from aiohttp import ClientSession

from blasmodcli.controller.game.group import GameCommandGroup
from blasmodcli.exceptions import NothingToDoException
from blasmodcli.utils import Message
from blasmodcli.utils.cli import Argument
from blasmodcli.utils.jobs import download
from blasmodcli.view import step, accept_or_cancel, NumberedList


def get_protontricks_executable() -> str | None:
    flatpak_exec = "com.github.Matoking.protontricks"
    fallback_exec = "protontricks"
    if which(flatpak_exec) is not None:
        Message.debug("Using the flatpak version of protontricks")
        return flatpak_exec
    elif which(fallback_exec) is not None:
        Message.debug("Using the fallback version of protontricks")
        return fallback_exec
    return None


class Configure(GameCommandGroup):
    """ Downloads and extract the modding tools for Blasphemous inside the game's folder. """

    yes: bool = Argument("-y", default=False, help="Skip the confirmation message.")

    archive: Path
    destination: Path
    dotnet_desktop_runtime: Path
    download_url: str
    script: str

    def post_init(self):
        if self.game.modding_tools is None:
            raise NothingToDoException("There is nothing to configure for this game, or it is not supported.")

        self.archive = self.directories.cache.resolve() / f"{self.game.id}-modding-tools.zip"
        Message.debug(f"The modding tools archive destination is '{self.archive}'.")
        self.destination = self.game.directory.resolve()
        self.download_url = self.game.modding_tools.url
        self.script = self.game.modding_tools.script_filename if self.game.modding_tools.script_filename is not None else "run_bepinex.sh"

    @step("Downloading the modding tools...")
    async def download_modding_tools(self):
        async with ClientSession() as session:
            await download(session, self.download_url, self.archive)
        Message.success("Successfully downloaded the modding tools!")

    @step("Extracting the modding tools...")
    def extract_modding_tools(self):
        with ZipFile(self.archive, "r") as zipfile:
            for info in zipfile.infolist():
                zipfile.extract(info, self.destination)
        Message.success("Modding tools successfully extracted!")

    # Methods for games native to Linux

    @step("Setting the execution permissions on the script file...")
    def setting_permissions(self):
        script = self.destination / self.script
        script.chmod(0o755)
        Message.success("Permissions correctly set!")

    # Methods for games not native to Linux

    def non_native_installation(self):
        number_of_deps = len(self.game.modding_tools.dependencies)
        if number_of_deps == 0:
            return

        protontricks_exec = get_protontricks_executable()
        if protontricks_exec is None:
            Message.info("It looks like protontricks is not installed on your system.")
            Message.info("For non native games that run through protons, protontricks is required to installed the necessary components for the modding tools to work.")
            Message.info("It can be installed through flatpak or with your distribution's package manager.")
            Message.info("Run this command later once it is installed, until then you cannot start to play with mods.")
            return

        if not self.yes:
            accept_or_cancel(f"Do you want to install all {number_of_deps} modding tools dependencies?")
        self.install_modding_tools_dependencies(protontricks_exec)

    @step("Installing the required dependencies for the modding tools...")
    def install_modding_tools_dependencies(self, protontricks_exec: str):
        dependencies = self.game.modding_tools.dependencies
        numbered_list = NumberedList(len(dependencies))
        for dependency in dependencies:
            progress = numbered_list.add_progress(f"Installing the {dependency.display_name}...")
            process = run([protontricks_exec, str(self.game.steamapp_id), dependency.name], capture_output=True)
            if process.returncode == 0:
                progress.success()
            else:
                progress.failure()
                Message.error(process.stderr.decode())
        Message.success("Successfully installed all modding tools dependencies!")

    async def handle(self) -> int:
        if not self.archive.is_file():
            if not self.yes:
                accept_or_cancel(f"Are you sure you want to download the modding tools at {self.download_url}?")
            await self.download_modding_tools()
        else:
            Message.success("Modding tools already downloaded.")

        if not self.yes:
            accept_or_cancel(f"Are you sure you want to extract the modding tools in the game's directory at {self.destination}?")
        self.extract_modding_tools()

        if self.game.linux_native:
            self.setting_permissions()
        else:
            self.non_native_installation()
        return 0
