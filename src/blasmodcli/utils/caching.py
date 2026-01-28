import re
from pathlib import Path

from blasmodcli.model import Mod, Version


ARCHIVE_FILENAME_PATTERN = re.compile(
    r"^(?P<game_id>[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*)"
    r"_(?P<source_name>[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*)"
    r"_(?P<mod_name>[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*)"
    r"_(?P<version>[0-9]+\.[0-9]+\.[0-9]+).zip$"
)


def mod_archive_name(mod: Mod, version: Version | None = None) -> str:
    """
    Returns the name of the archive file for a mod.
    If no version is specified, used a wildcard to represent archives for every version of a mod.
    :param mod: The mod from which the archive name is created.
    :param version: The version of the archive, defaults to None (*).
    :return: The name of the archive with its .zip suffix.
    """
    v = str(version) if version is not None else "*"
    return f"{mod.game_id}_{mod.source_name}_{mod.name}_{v}.zip"


class CacheDirectory:

    def __init__(self, directory: Path):
        self.directory = directory

    def get_all_archives(self, mod: Mod) -> list[Path]:
        archives = []
        for entry in self.directory.glob(mod_archive_name(mod)):
            if not entry.is_file():
                continue
            archives.append(entry)
        return archives

    def get_all_cached_versions(self, mod: Mod) -> list[Version]:
        versions = []
        for archive in self.get_all_archives(mod):
            match = ARCHIVE_FILENAME_PATTERN.match(archive.name)
            if match is None:
                continue
            versions.append(Version.from_tag(match.group("version")))
        return versions

    def get_archive(self, mod: Mod, version: Version) -> Path:
        return self.directory / mod_archive_name(mod, version)

    def get_latest_version(self, mod: Mod) -> Version | None:
        versions = self.get_all_cached_versions(mod)
        latest = None
        for version in versions:
            if latest is None or version > latest:
                latest = version
        return latest

    def has(self, mod: Mod, version: Version | None = None) -> bool:
        if version is None:
            return len(self.get_all_cached_versions(mod)) != 0
        return self.get_archive(mod, version).is_file()

    def remove_all_versions(self, mod: Mod):
        for archive in self.get_all_archives(mod):
            archive.unlink()

    def remove_version(self, mod: Mod, version: Version):
        self.get_archive(mod, version).unlink()
