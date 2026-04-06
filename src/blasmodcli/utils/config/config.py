from pathlib import Path

from blasmodcli.repositories import TableRepositories
from blasmodcli.utils import Directories
from blasmodcli.utils.config.games import GameConfiguration
from blasmodcli.utils.config.sources import SourceConfiguration


class Configuration:

    def __init__(self, directory: Path, tables: TableRepositories):
        self.directory = Directories.require(directory)
        self.tables = tables
        self.file = directory / "general.toml"
        self.games = GameConfiguration(self.directory / "games", self.tables.games)
        self.sources = SourceConfiguration(self.directory / "sources", self.tables.sources)
