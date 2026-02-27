from collections.abc import Sequence, Generator
from pathlib import Path
from re import Match

from blasmodcli.model import Game, Mod, ModVersion, Version
from blasmodcli.repositories.filesystems.entry import Entry, FILENAME_PATTERN
from blasmodcli.repositories.repository import IRepository
from blasmodcli.utils import Directories


class FileSystemRepository(IRepository[Path]):

    def __init__(
            self,
            directory: Path,
            default_extension: str,
            accepted_extensions: Sequence[str] | None = None
    ):
        self.directory = Directories.require(directory)
        self.default_extension = default_extension
        self.accepted_extensions = accepted_extensions if accepted_extensions is not None else (self.default_extension,)

    def get_all(self) -> list[Path]:
        files = []
        for entry in self.directory.iterdir():
            if not entry.is_file():
                continue
            files.append(entry)
        return files

    def get_all_entries(self) -> Generator[Entry]:
        for file in self.get_all():
            entry = self.entry(file)
            if entry is not None:
                yield entry

    def get_all_versions(self, game: Game) -> list[ModVersion]:
        mod_versions = []
        for mod in game.mods:
            versions = self.get_all_versions_of(mod)
            for version in versions:
                mod_versions.append(ModVersion(mod, version))
        return mod_versions

    def get_all_latest_versions(self, game: Game) -> list[ModVersion]:
        mod_versions = []
        for mod in game.mods:
            version = self.get_latest_version(mod)
            if version is None:
                continue
            mod_versions.append(ModVersion(mod, version))
        return mod_versions

    def get_all_versions_of(self, mod: Mod) -> list[Version]:
        versions: list[Version] = []
        for entry in self.get_entries_for(mod):
            versions.append(entry.version)
        return versions

    def get_entries_for(self, mod: Mod, version: Version | None = None) -> Generator[Entry]:
        for file in self.get_files_for(mod, version):
            entry = self.entry(file)
            if entry is not None:
                yield entry

    def get_entry_for(self, mod_version: ModVersion) -> Entry | None:
        file = self.get_file_for(mod_version)
        if file is None:
            return None
        return self.entry(file)

    def get_files_for(self, mod: Mod, version: Version | None = None) -> Generator[Path]:
        for file in self.directory.glob(self.filename(mod, version)):
            if file.is_file():
                yield file

    def get_file_for(self, mod_version: ModVersion) -> Path | None:
        for file in self.get_files_for(mod_version.mod, mod_version.version):
            return file
        return None

    def get_latest_version(self, mod: Mod) -> Version | None:
        versions = self.get_all_versions_of(mod)
        latest = None
        for version in versions:
            if latest is None or version > latest:
                latest = version
        return latest

    def entry(self, file: Path) -> Entry | None:
        match = self.match(file)
        if match is None:
            return None
        return Entry(
            match.group("game_id"),
            match.group("source_name"),
            match.group("mod_name"),
            Version.from_tag(match.group("version")),
            match.group("ext")
        )

    def file(self, mod_version: ModVersion) -> Path:
        return self.directory / self.filename(mod_version.mod, mod_version.version)

    def filename(self, mod: Mod, version: Version | None = None) -> str:
        """
        Returns the name of the archive file for a mod.
        If no version is specified, used a wildcard to represent archives for every version of a mod.
        :param mod: The mod from which the archive name is created.
        :param version: The version of the archive, defaults to None (*).
        :return: The name of the archive with its .zip suffix.
        """
        v = str(version) if version is not None else "*"
        return f"{mod.game_id}_{mod.source_name}_{mod.name}_{v}.{self.default_extension}"

    def has(self, mod: Mod, version: Version | None = None):
        for _ in self.get_files_for(mod, version):
            return True
        return False

    def match(self, file: Path) -> Match | None:
        match = FILENAME_PATTERN.match(file.name)
        if match is None:
            return None
        if match.group("ext") not in self.accepted_extensions:
            return None
        return match
