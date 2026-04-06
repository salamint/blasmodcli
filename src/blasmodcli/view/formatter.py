from blasmodcli.model import Mod, Version, ModVersion
from blasmodcli.repositories import FileSystemRepositories

from blasmodcli.utils.colors import Color
from blasmodcli.view.table import Table


SEPARATOR = ", "


class DateFormat:
    SIMPLE = "%Y-%m-%d"
    DETAILED = "%A, %e %B %Y"


def format_bool(boolean: bool) -> str:
    if boolean:
        return Color.fmt("Yes", Color.GREEN)
    return Color.fmt("No", Color.RED)


def format_mod_name(mod: Mod, display_name: bool = True) -> str:
    return Color.fmt(mod.display_name if display_name else mod.name, Color.BLUE if mod.is_library else Color.WHITE)


def format_mod_authors_list(mod: Mod) -> str:
    return SEPARATOR.join(author.name for author in mod.authors)


def format_mod_dependencies_list(mod: Mod) -> str:
    return SEPARATOR.join(dep.dependency.name for dep in mod.dependencies)


class Formatter:

    def __init__(self, fs: FileSystemRepositories, local: bool):
        self.fs = fs
        self.local = local

    def get_version(self, mod_version: ModVersion) -> str:
        if self.local:
            installation = self.fs.installations.get(mod_version)
            if installation is None:
                return "unknown"
            return str(installation.version)
        return str(mod_version.version)

    def get_full_name(self, mod: Mod, version: Version | None = None) -> str:
        source = Color.fmt(f"{mod.source_name}", Color.MAGENTA)
        name = format_mod_name(mod, display_name=False)
        version = Color.fmt(self.get_version(ModVersion(mod, version)), Color.YELLOW)
        return f"{source}/{name}:{version}"

    def summary(self, mod: Mod, version: Version | None = None):
        authors = Color.fmt(format_mod_authors_list(mod), Color.GREEN)
        print(f"{self.get_full_name(mod, version)} by {authors}\n    {mod.description}")

    def print_info(self, mod: Mod, version: Version | None = None):
        is_cached = self.fs.cache.has(mod, version)
        installation = self.fs.installations.get(ModVersion(mod, version))
        is_installed = installation is not None

        table = Table(f"Displaying information about {mod.display_name} in version {version}")
        table.add_row("Game", f"{mod.game.title} ({mod.game_id})")
        table.add_row("Source", mod.source_name)
        table.add_row("Name", format_mod_name(mod, display_name=False))
        table.add_row("Full name", self.get_full_name(mod, version))
        table.add_separator()
        table.add_row("Display name", format_mod_name(mod))
        table.add_row("Description", mod.description)
        table.add_row("Is a library", mod.is_library, Color.YELLOW)
        table.add_row("Authors", format_mod_authors_list(mod), Color.GREEN)
        table.add_row("Repository", mod.repository, Color.BLUE)
        table.add_row("Dependencies", format_mod_dependencies_list(mod))
        table.add_row("Release date", mod.release_date.strftime(DateFormat.DETAILED))
        table.add_row("Latest version", mod.latest_version, Color.YELLOW)
        table.add_separator()
        table.add_row("Cached", format_bool(is_cached))
        table.add_row("Installed", format_bool(is_installed))
        if is_installed:
            table.add_row("Installed version", installation.version, Color.YELLOW)
        table.print()
