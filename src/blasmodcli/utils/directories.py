import os
from pathlib import Path


class Directories:

    XDG_CACHE = Path.home() / ".cache"
    XDG_CONFIG = Path.home() / ".config"
    XDG_DATA = Path.home() / ".local" / "share"
    XDG_STATE = Path.home() / ".local" / "state"

    @staticmethod
    def get_steam_data() -> Path:
        default = Directories.XDG_DATA / "Steam"
        env_var = os.environ.get("STEAM_DATA_PATH")
        if env_var is None:
            return default

        steam_data_path = Path(env_var)
        if steam_data_path.is_dir():
            return steam_data_path
        return default

    @staticmethod
    def get_steam_apps() -> Path:
        return Directories.get_steam_data() / "steamapps"

    @staticmethod
    def get_steam_game_directory(game_name: str) -> Path:
        return Directories.get_steam_apps() / "common" / game_name

    @staticmethod
    def require(directory: Path):
        if not directory.is_dir():
            directory.mkdir(parents=True)

    def __init__(self, exec_name: str):
        self.cache = Directories.XDG_CACHE / exec_name
        self.config = Directories.XDG_CONFIG / exec_name
        self.data = Directories.XDG_DATA / exec_name
        self.state = Directories.XDG_STATE / exec_name
