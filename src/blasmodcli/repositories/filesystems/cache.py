from pathlib import Path

from blasmodcli.model import Mod, ModVersion

from blasmodcli.repositories.filesystems.filesystem import FileSystemRepository


class CacheRepository(FileSystemRepository):

    def __init__(self, directory: Path):
        super().__init__(directory, "zip")

    def remove_all_versions(self, mod: Mod):
        for archive in self.get_files_for(mod):
            archive.unlink()

    def remove_version(self, mod_version: ModVersion):
        self.file(mod_version).unlink()
