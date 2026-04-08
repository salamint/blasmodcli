import os
from pathlib import Path

from blasmodcli.utils.message import logger

CUSTOM_PATH_ENV_VAR = "STEAM_DATA_PATH"


class Directories:

    XDG_CACHE = Path.home() / ".cache"
    XDG_CONFIG = Path.home() / ".config"
    XDG_DATA = Path.home() / ".local" / "share"
    XDG_STATE = Path.home() / ".local" / "state"

    TMP_STORAGE = Path("/tmp")

    @staticmethod
    def get_steam_data() -> Path:
        default = Directories.XDG_DATA.resolve() / "Steam"
        env_var = os.environ.get(CUSTOM_PATH_ENV_VAR)
        if env_var is None:
            return default

        steam_data_path = Path(env_var).resolve()
        if steam_data_path.is_dir():
            return steam_data_path

        logger.warning(f"The directory specified by the {CUSTOM_PATH_ENV_VAR} environment variable does not exist, using the default {default} directory instead.")
        return default

    @staticmethod
    def get_steam_apps() -> Path:
        return Directories.get_steam_data() / "steamapps"

    @staticmethod
    def get_steam_game_directory(game_name: str) -> Path:
        return Directories.get_steam_apps() / "common" / game_name

    @staticmethod
    def require(path: Path, parent: bool = False):
        directory = path.parent if parent else path
        if not directory.is_dir():
            directory.mkdir(parents=True)
        return path

    def __init__(self, exec_name: str):
        self.cache = Directories.XDG_CACHE / exec_name
        self.config = Directories.XDG_CONFIG / exec_name
        self.data = Directories.XDG_DATA / exec_name
        self.state = Directories.XDG_STATE / exec_name
        self.temp = Directories.TMP_STORAGE / exec_name
