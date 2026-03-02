from .cache import CacheRepository
from .filesystem import FileSystemRepository
from .installations import InstallationRepository

from blasmodcli.utils import Directories


class FileSystemRepositories:

    def __init__(self, directories: Directories):
        self.cache = CacheRepository(directories.cache / "mods")
        self.installations = InstallationRepository(directories.data / "installations")
