from pathlib import Path


class Directories:

    XDG_CACHE = Path.home() / ".cache"
    XDG_CONFIG = Path.home() / ".config"
    XDG_DATA = Path.home() / ".local" / "share"
    XDG_STATE = Path.home() / ".local" / "state"

    STEAM_DATA = XDG_DATA / "Steam"
    STEAM_APPS = STEAM_DATA / "steamapps"

    @staticmethod
    def get_steam_game_directory(game_name: str) -> Path:
        return Directories.STEAM_APPS / "common" / game_name

    @staticmethod
    def require(directory: Path):
        if not directory.is_dir():
            directory.mkdir(parents=True)

    def __init__(self, exec_name: str):
        self.cache = Directories.XDG_CACHE / exec_name
        self.config = Directories.XDG_CONFIG / exec_name
        self.data = Directories.XDG_DATA / exec_name
        self.state = Directories.XDG_STATE / exec_name
