from sqlalchemy import Engine

from blasmodcli.repositories import FileSystemRepositories, TableRepositories
from blasmodcli.utils import Directories
from blasmodcli.utils.config import Configuration


class CommandContext:

    def __init__(self, directories: Directories, engine: Engine):
        self.directories = directories
        self.fs = FileSystemRepositories(self.directories)
        self.tables = TableRepositories(engine)
        self.config = Configuration(self.directories.config, self.tables)
