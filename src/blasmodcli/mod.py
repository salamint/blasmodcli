from enum import IntEnum
from pathlib import Path
from shutil import unpack_archive
from time import strptime, struct_time, strftime
from urllib.request import urlretrieve
from requests import get as request, HTTPError

from blasmodcli.exceptions import DoneException, CancelException
from blasmodcli.utils import Color, Message, Table, Counter, Directories
from blasmodcli.version import Version
import blasmodcli.games.game


AUTHORS_SEPARATOR = " && "


class DateFormat:
    SIMPLE = "%Y-%m-%d"
    DETAILED = "%A, %e %B %Y"


class ModState(IntEnum):
    NONE = 0
    INSTALLED = 1
    ACTIVATED = 2


# TODO: add uninstall method
# TODO: add upgrade method
class Mod:

    @classmethod
    def from_raw_data(cls, game: 'blasmodcli.games.game.Game', data: dict):
        authors = data["Author"].replace(", ", AUTHORS_SEPARATOR).replace(", && ", AUTHORS_SEPARATOR)
        repository = f"https://github.com/{data['GithubAuthor']}/{data['GithubRepo']}"
        response = request(f"{repository}/releases/latest")
        if not response.ok:
            return None
        return cls(
            game,
            data["Name"],
            [author.strip() for author in authors.split(AUTHORS_SEPARATOR)],
            data["Description"],
            strptime(data["InitialReleaseDate"], DateFormat.SIMPLE),
            repository,
            data["PluginFile"],
            data.get("Dependencies", []),
            Version.from_string(response.url.split("/")[-1])
        )

    @classmethod
    def deserialize(cls, game: 'blasmodcli.games.game.Game', data: dict):
        return cls(
            game,
            data["name"],
            data["authors"],
            data["description"],
            release_date=strptime(data["release_date"], DateFormat.SIMPLE),
            repository=data["repository"],
            plugin_file=data["plugin_file"],
            dependencies=data["dependencies"],
            version = Version.from_string(data["version"])
        )

    def __init__(
            self,
            game: 'blasmodcli.games.game.Game',
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
    def authors_string(self) -> str:
        return ", ".join(self.authors)

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
            raise DoneException("This mod was not activated.")

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
                raise CancelException("Installation cancelled.")

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

    def is_activated(self) -> bool:
        return self.plugin_file.is_file()

    def is_installed(self) -> bool:
        return self.get_installed_version() is not None

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

    def print(self, local: bool):
        if local:
            version = self.get_installed_version()
        else:
            version = self.version

        name = Color.fmt(self.name, Color.WHITE)
        version = Color.fmt(version, Color.YELLOW)
        authors = Color.fmt(self.authors_string, Color.GREEN)
        print(f"{name} {version} by {authors}\n    {self.description}")

    def print_info(self):
        installed = Color.fmt("No", Color.RED)
        activated = Color.fmt("No", Color.RED)
        if self.get_installed_version():
            installed = Color.fmt("Yes", Color.GREEN)
            if self.is_activated():
                activated = Color.fmt("Yes", Color.GREEN)

        table = Table()
        table.add_row("Name", self.name)
        table.add_row("Description", self.description)
        table.add_row("Authors", self.authors_string, Color.GREEN)
        table.add_row("Repository", self.repository, Color.BLUE)
        table.add_row("Dependencies", ", ".join(dep.name for dep in self.dependencies))
        table.add_row("Release date", strftime(DateFormat.DETAILED, self.release_date))
        table.add_row("Version", self.version, Color.YELLOW)
        table.add_row("Installed", installed)
        table.add_row("Activated", activated)
        table.print()

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

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "authors": self.authors,
            "description": self.description,
            "release_date": strftime(DateFormat.SIMPLE, self.release_date),
            "repository": self.repository,
            "plugin_file": self.plugin_file.name,
            "dependencies": self.__dependencies,
            "version": str(self.version)
        }

    def unpack_archive(self, reactivate: bool = True) -> int:
        if self.is_activated() and not reactivate:
            return 0
        if not self.is_installed():
            raise FileNotFoundError(f"Mod '{self.name}' is not installed!")
        unpack_archive(self.get_installed_archive(), self.game.modding_directory, "zip")
        return 0
