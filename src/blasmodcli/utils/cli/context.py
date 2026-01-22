from dataclasses import dataclass

from blasmodcli.repositories import Warehouse
from blasmodcli.utils import Directories
from blasmodcli.utils.config import Configuration


@dataclass
class CommandContext:
    config: Configuration
    directories: Directories
    warehouse: Warehouse
