from enum import IntEnum
from pathlib import Path
from shutil import unpack_archive
from time import struct_time
from urllib.request import urlretrieve
from requests import get as request, HTTPError

from blasmodcli.exceptions import NothingToDoException, UserCancelException
from blasmodcli.utils import Color, Directories
from blasmodcli.view import Message, Counter
from blasmodcli.model.version import Version


AUTHORS_SEPARATOR = " && "


class ModState(IntEnum):
    NONE = 0
    INSTALLED = 1
    ACTIVATED = 2


# TODO: add uninstall method
# TODO: add upgrade method
class Mod:

    def __init__(
            self,
            game: 'Game',
            name: str,
            authors: list[str],
            description: str,
            release_date: struct_time,
            repository: str,
            plugin_file: str,
            dependencies: list[str],
            version: 'Version'
    ):
        self.game = game
        self.name = name
        self.authors = authors
        self.description = description
        self.release_date = release_date
        self.repository = repository
        self.plugin_file = game.modding_directory.plugins / plugin_file
        self.__dependencies = dependencies
        self.version = version

    def __repr__(self) -> str:
        return f"<{self.name} ({self.version})>"

    # Properties

    @property
    def archive(self) -> Path:
        return self.game.mods_directory / f"{self.name}-{self.version}.zip"

    @property
    def dependencies(self) -> set['Mod']:
        return {self.game.get_mod(dep) for dep in self.__dependencies}

    def activate(self, reactivate: bool = False, recursive: bool = True) -> int:
        if not recursive:
            p = Message.progress(f"Activating mod '{self.name}'")
            try:
                self.unpack_archive(reactivate)
            except Exception as e:
                p.failure()
                raise e
            p.success()
            return 0

        dependencies = self.resolve_dependencies(max_state=ModState.INSTALLED)
        counter = Counter(len(dependencies))
        for dependency in dependencies:
            p = counter.add_progress(f"Activating mod '{dependency.name}'")
            try:
                dependency.unpack_archive(reactivate)
            except Exception as e:
                p.failure()
                raise e
            p.success()
        return 0

    # TODO: recursive
    # TODO: also deactivate mods that depend on this one
    def deactivate(self, recursive: bool = True):
        if not self.is_activated() and not recursive:
            raise NothingToDoException("This mod was not activated.")

        p = Message.progress(f"Deactivating mod '{self.name}'")
        try:
            self.plugin_file.unlink()
        except FileNotFoundError as e:
            p.failure()
            raise FileNotFoundError(f"The mod's plugin file was not found: {e.filename}")
        p.success()
        return 0

    def install(self, activate_after: bool = True, force: bool = False) -> int:
        Directories.require(self.game.mods_directory)
        p = Message.progress("Resolving dependencies")
        dependencies = self.resolve_dependencies(max_state=ModState.NONE)
        if force and self not in dependencies:
            dependencies.append(self)
        total = len(dependencies)
        p.status("DONE", Color.GREEN)

        if total > 0:
            Message.info("Mods to install:")
            bullet = Color.fmt("-", Color.BLUE)
            for dependency in dependencies:
                name = Color.fmt(dependency.name, Color.WHITE)
                version = Color.fmt(dependency.version, Color.YELLOW)
                print(f"    {bullet} {name} {version}")

            if not Message.ask("Do you want to continue the installation?", default=True):
                raise UserCancelException("Installation cancelled.")

            failed = []
            counter = Counter(total)
            for i, dependency in enumerate(dependencies):
                p = counter.add_progress(f"Downloading {Color.fmt(dependency.name, Color.WHITE)}...")
                archive_url = dependency.get_release_archive_url()
                if archive_url is None:
                    p.failure()
                    failed.append(dependency)
                elif urlretrieve(archive_url, dependency.archive):
                    p.success()
                else:
                    p.failure()
                    failed.append(dependency)

            if len(failed) > 0:
                raise HTTPError("Failed to download dependencies: " + ", ".join(failed))

            Message.success(f"Dependencies successfully installed!")
        else:
            Message.success("Every dependency is already installed!")

        if activate_after:
            return self.activate()
        return 0

    def get_installed_archive(self) -> Path | None:
        try:
            for archive in self.game.mods_directory.iterdir():
                components = archive.stem.split("-")
                if len(components) == 1:
                    continue
                if "-".join(components[:-1]) == self.name:
                    return archive
            return None
        except FileNotFoundError:
            return None

    def get_installed_version(self) -> 'Version | None':
        archive = self.get_installed_archive()
        if archive is None:
            return None
        components = archive.stem.split("-")
        version = Version.from_string(components[-1])
        return version

    def get_release_page_url(self, version: 'Version | None' = None) -> str | None:
        version = version if version is not None else self.version
        base_url = f"{self.repository}/releases/tag"
        for url in (f"{version}", f"v{version}"):
            url = base_url + "/" + url
            response = request(url)
            if response.ok:
                return url
        return None

    def get_release_archive_url(self, version: 'Version | None' = None) -> str | None:
        version = version if version is not None else self.version
        base_url = self.get_release_page_url(version).replace("/tag/", "/download/")
        name = self.name.replace(' ', '')
        if base_url is None:
            return None
        for url in (f"{name}.zip", f"{name}.v{version}.zip", f"{name}-v{version}.zip"):
            url = base_url + "/" + url
            response = request(url)
            if response.ok:
                return url
        return None

    def get_state(self) -> 'ModState':
        if self.is_activated():
            return ModState.ACTIVATED
        elif self.is_installed():
            return ModState.INSTALLED
        return ModState.NONE

    def resolve_dependencies(self, max_state: 'ModState' = ModState.ACTIVATED) -> list['Mod']:
        dependencies = []
        queue = [self]
        while len(queue) != 0:
            mod = queue.pop(0)
            for dependency in mod.dependencies:
                if dependency not in dependencies and dependency not in queue:
                    queue.append(dependency)
            if mod.get_state() <= max_state:
                dependencies.insert(0, mod)
        return dependencies

    def unpack_archive(self, reactivate: bool = True) -> int:
        if self.is_activated() and not reactivate:
            return 0
        if not self.is_installed():
            raise FileNotFoundError(f"Mod '{self.name}' is not installed!")
        unpack_archive(self.get_installed_archive(), self.game.modding_directory, "zip")
        return 0


from blasmodcli.games.game import Game
