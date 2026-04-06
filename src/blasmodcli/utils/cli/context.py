from dataclasses import dataclass

from blasmodcli.repositories import FileSystemRepositories, TableRepositories
from blasmodcli.utils import Directories
from blasmodcli.utils.config import Configuration


@dataclass
class CommandContext:
    config: Configuration
    directories: Directories
    fs: FileSystemRepositories
    tables: TableRepositories
