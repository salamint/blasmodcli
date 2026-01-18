from pathlib import Path

from blasmodcli.repositories import Warehouse
from blasmodcli.utils import Directories
from blasmodcli.utils.config.games import GameConfiguration
from blasmodcli.utils.config.sources import SourceConfiguration


class Configuration:

    def __init__(self, directory: Path, warehouse: Warehouse):
        self.directory = Directories.require(directory)
        self.warehouse = warehouse
        self.file = directory / "general.toml"
        self.games = GameConfiguration(self.directory / "games", self.warehouse.games)
        self.sources = SourceConfiguration(self.directory / "sources", self.warehouse.mod_sources)
