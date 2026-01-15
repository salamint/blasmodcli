from dataclasses import dataclass

from blasmodcli.config import Configuration
from blasmodcli.repositories import Warehouse
from blasmodcli.utils import Directories


@dataclass
class CommandContext:
    config: Configuration
    directories: Directories
    warehouse: Warehouse
