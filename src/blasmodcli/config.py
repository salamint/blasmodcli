import tomllib
from pathlib import Path

from blasmodcli.model import Game
from blasmodcli.repositories import GameRepository
from blasmodcli.utils import Directories


class Configuration:

    def __init__(self, directory: Path):
        self.directory = Directories.require(directory)
        self.games: dict[str, Game] = {}

    @property
    def games_config(self) -> Path:
        return self.directory / "games.toml"

    @property
    def sources_directory(self) -> Path:
        return self.directory / "sources"

    def load_games(self, repository: GameRepository):
        if not self.games_config.is_file():
            raise FileNotFoundError(f"Missing games configuration file '{self.games_config}'")
        with self.games_config.open("rb") as file:
            data = tomllib.load(file)
            for key, attrs in data.items():
                game = Game(**attrs)
                self.games[key] = game
                repository.sync(game)
