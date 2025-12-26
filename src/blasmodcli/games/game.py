from abc import ABC, abstractmethod
from pathlib import Path
from requests import get as request
from shutil import make_archive, rmtree
from time import localtime, strftime
import json

from blasmodcli.exceptions import CancelException, DoneException
from blasmodcli.games.modding_tools import ModdingTools
from blasmodcli.utils import Directories, Message, Color, Counter
from blasmodcli.model.version import Version
import blasmodcli.mod

MODDING_INSTALLER_REPO = "https://github.com/BrandenEK/Blasphemous.Modding.Installer"


class ModdingDirectory(Path):

    def __init__(self, game: 'Game | Path', *args):
        if isinstance(game, Game):
            super().__init__(game.directory / "Modding")
            self.mods = self.joinpath("mods")
            self.plugins = self.joinpath("plugins")
            self.skins = self.joinpath("skins")
        else:
            super().__init__(game, *args)


class Game(ABC):

    all: dict[str, 'Game'] = {}

    def __init__(
            self,
            name: str,
            tool_name: str,
            mod_loader: str,
            modding_tools_url: str,
            saves_directory: Path,
            is_native: bool = True
    ):
        if Game.all.get(name) is not None:
            raise ValueError(f"There is already a tool named '{name}'!")
        Game.all[name] = self

        self.tool_name = tool_name
        self.name = name
        self.is_native = is_native
        self.tool_directories = Directories(self.tool_name)
        self.directory = Directories.get_steam_game_directory(name)
        self.modding_directory = ModdingDirectory(self)
        self.modding_tools = ModdingTools(self, mod_loader, modding_tools_url)
        self.mods_directory = self.tool_directories.data / "mods"
        self.saves_directory = saves_directory
        self.database_file = self.tool_directories.cache / "mods.json"
        self.mod_sources: list[str] = []
        self.mods: dict[str, 'blasmodcli.mod.Mod'] = {}

    def add_mod_source(self, url: str):
        self.mod_sources.append(url)

    def backup_saves(self, destination: Path | None = None) -> int:
        Message.info("Backing up saves data...")
        if destination is None:
            destination = Path.cwd()
        if destination.is_dir():
            destination = destination / f"BlasphemousSavesBackup_{strftime('%Y-%m-%d_%Hh%Mm%Ss', localtime())}"
        elif destination.suffix == ".zip":
            destination = destination.with_suffix("")

        make_archive(str(destination), "zip", self.saves_directory)
        Message.success(f"Saves data backed up at '{destination}'!")
        return 0

    def clear_modding_directory(self, force: bool = False) -> int:
        if not self.modding_directory.is_dir():
            raise DoneException("Nothing to delete.")

        if not force:
            if not Message.ask(
                    "Are you sure you want to delete the 'Modding' directory?"
                    " This will deactivate every mod, and remove current configurations and keybindings."
            ):
                raise CancelException("Operation cancelled.")

        rmtree(self.modding_directory)
        return 0

    @abstractmethod
    def configure_modding_tools(self) -> int:
        raise NotImplementedError

    def fetch_latest_modding_tools_version(self) -> int:
        p = Message.progress("Fetching latest modding tools version")
        response = request(self.modding_tools.version_url)
        if not response.ok:
            p.failure()
            return 1

        latest = Version.from_string(response.text)
        p.version(latest)
        cfg_cmd = Color.fmt("configure", Color.WHITE)
        if self.modding_tools.version_file.is_file():
            with self.modding_tools.version_file.open("r") as file:
                current = Version.from_string(file.read())
                if current < latest:
                    Message.info(
                        f"An update for the modding tools is available!"
                        f" Download it now by running the {cfg_cmd} command."
                    )
        elif self.modding_tools.are_installed():
            Message.warning(
                f"The currently installed modding tools don't have version information."
                f" To make sure it is up to date, run the {cfg_cmd} command."
            )
        else:
            Message.info(
                f"You don't have the modding tools installed, you need them to run mods on your game."
                f" To install the modding tools, run the {cfg_cmd} command."
            )
        return 0

    def fetch_mods_data_from_sources(self) -> list[dict]:
        mods_data: list[dict] = []
        counter = Counter(len(self.mod_sources))
        for source in self.mod_sources:
            p = counter.add_progress(source)
            response = request(source)
            if response.ok:
                database = response.json()
                mods_data.extend(database)
            p.bool(response.ok)
        return mods_data

    def get_mod(self, name: str) -> 'blasmodcli.mod.Mod':
        mod = self.mods.get(name)
        if mod is None:
            raise KeyError(f"No mod named '{name}' found.")
        return mod

    def is_installed(self) -> bool:
        return self.directory.is_dir()

    def list_mods(self, state: 'blasmodcli.mod.ModState' = blasmodcli.mod.ModState.NONE) -> list[blasmodcli.mod.Mod]:
        mod_list: list[blasmodcli.mod.Mod] = []
        for mod in self.mods.values():
            if mod.get_state() >= state:
                mod_list.append(mod)
        return mod_list

    def load_mods(self):
        try:
            with self.database_file.open("r") as db:
                for data in json.load(db):
                    mod = blasmodcli.mod.Mod.deserialize(self, data)
                    self.mods[mod.name] = mod
        except FileNotFoundError:
            update = Color.fmt("update", Color.WHITE)
            raise FileNotFoundError(f"Mod database file not found. Make sure to {update} the mod database.")

    def search(self, terms: list[str]) -> list['blasmodcli.mod.Mod']:
        matching_mods: list[blasmodcli.mod.Mod] = []
        for mod in self.list_mods():
            for term in terms:
                term = term.lower()
                if term in mod.name.lower() or term in mod.description.lower():
                    matching_mods.append(mod)
                    break
        return matching_mods

    def update_database(self) -> int:
        Message.info("Fetching mods database(s)...")
        mods_data = self.fetch_mods_data_from_sources()

        Message.info("Fetching latest mod version...")
        counter = Counter(len(mods_data))
        mods_list: list[blasmodcli.mod.Mod] = []
        for data in mods_data:
            p = counter.add_progress(data["Name"])
            mod = blasmodcli.mod.Mod.from_raw_data(self, data)
            if mod is not None:
                mods_list.append(mod)
                p.version(mod.version)
            else:
                p.failure()

        Message.info("Saving mod database...")
        Directories.require(self.tool_directories.cache)
        with self.database_file.open("w") as db:
            json.dump([mod.serialize() for mod in mods_list], db, indent=2)
        Message.success("Update successful!")
        return 0
