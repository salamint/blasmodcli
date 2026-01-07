from shutil import unpack_archive
from urllib.request import urlretrieve
from requests import HTTPError

from blasmodcli.exceptions import CancelException, DoneException
from blasmodcli.games.game import Game
from blasmodcli.utils import Color, Directories, Message, MODDING_INSTALLER_REPOSITORY
from blasmodcli.model.version import Version


class Blasphemous(Game):

    def __init__(self):
        super().__init__(
            "Blasphemous",
            "blasmodcli",
            "BepInEx",
            "https://github.com/BrandenEK/Blasphemous.ModdingTools",
            Directories.XDG_CONFIG / "unity3d" / "TheGameKitchen" / "Blasphemous" / "Savegames",
            is_native=True
        )
        self.bepinex_script = self.directory / "run_bepinex.sh"

    def configure_modding_tools(self) -> int:
        latest = self.modding_tools.get_latest_version()
        current = self.modding_tools.get_current_version()
        up_to_date = current is not None and current >= latest

        if self.modding_directory.is_dir() and self.modding_tools.are_installed() and up_to_date:
            raise DoneException("Modding tools are already up to date.")

        self.download_modding_tools()
        self.warn_and_suggest_backing_up()
        self.extract_modding_tools(latest)
        Message.success("Modding tools successfully installed!")
        return 0

    def download_modding_tools(self):
        p = Message.progress("Downloading the modding tools")
        if not urlretrieve(self.modding_tools.archive_url, self.modding_tools.archive_file):
            p.failure()
            raise HTTPError("Failed to download the modding tools: ")
        p.success()

    def extract_modding_tools(self, version: 'Version'):
        p = Message.progress("Extracting modding tools...")
        try:
            unpack_archive(self.modding_tools.archive_file, self.directory)
            self.bepinex_script.chmod(0o755)
            Directories.require(self.tool_directories.data)
            with self.modding_tools.version_file.open("w") as file:
                file.write(str(version))
        except Exception as e:
            p.failure()
            raise e
        p.success()

    def warn_and_suggest_backing_up(self):
        Message.error(f"""IMPORTANT NOTICE
    The modding tools is an archive containing files, that will be
    extracted {Color.WHITE}directly inside the game's directory{Color.RESET}.
    This procedure should not fail, and should not replace any of the game's file.

    {Color.WHITE}HOWEVER, THE AUTHOR AND THE CONTRIBUTORS OF THIS SCRIPT DENY ALL RESPONSIBILITY
    IF THE GAME OR YOUR PROGRESSION IS DAMAGED IN ANYWAY DURING THIS PROCEDURE.{Color.RESET}

    If the game does not start after this step, try following the steps here:
    {Color.fmt(MODDING_INSTALLER_REPOSITORY, Color.BLUE)}
    If neither work, uninstall then reinstall your game.

    {Color.WHITE}IN ANY CASE, WE RECOMMEND YOU TO BACKUP YOUR SAVE FILES.{Color.RESET}""")
        if Message.ask(
                "Would you like to backup your saves before hand? You can also backup your saves directly from Steam."
        ):
            self.backup_saves()

        if not Message.ask("Would you like to proceed to the extraction?"):
            raise CancelException("Installation process cancelled.")
