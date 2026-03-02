from pathlib import Path

from blasmodcli.model import Game, Installation, ModVersion
from blasmodcli.repositories.filesystems.filesystem import FileSystemRepository


class InstallationRepository(FileSystemRepository):

    def __init__(self, directory: Path):
        super().__init__(directory, "txt")

    def get(self, mod_version: ModVersion) -> Installation | None:
        entry = self.get_file_for(mod_version)
        if entry is None:
            return None
        return Installation(entry, mod_version)

    def get_upgrades(self, game: Game) -> list[ModVersion]:
        upgrades = []
        for mod, version in self.get_all_latest_versions(game):
            if version < mod.latest_version:
                upgrades.append(ModVersion(mod, version))
        return upgrades

    def new(self, mod_version: ModVersion) -> Installation:
        installation = Installation(self.file(mod_version), mod_version)
        return installation
