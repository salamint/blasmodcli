from blasmodcli.model import Mod, Version
from blasmodcli.utils.caching import CacheDirectory

from blasmodcli.utils.colors import Color
from blasmodcli.view.table import Table


class DateFormat:
    SIMPLE = "%Y-%m-%d"
    DETAILED = "%A, %e %B %Y"


def format_bool(boolean: bool) -> str:
    if boolean:
        return Color.fmt("Yes", Color.GREEN)
    return Color.fmt("No", Color.RED)


def format_mod_name(mod: Mod, display_name: bool = True) -> str:
    return Color.fmt(mod.display_name if display_name else mod.name, Color.BLUE if mod.is_library else Color.WHITE)


class Formatter:

    def __init__(self, mod: Mod, version: Version | None = None):
        self.mod = mod
        self.version = version

    def authors_list(self) -> str:
        return ", ".join(author.name for author in self.mod.authors)

    def get_version(self, local: bool) -> str:
        if local:
            if self.mod.installation is not None:
                return str(self.mod.installation.version)
            return "unknown"
        return str(self.mod.latest_version)

    def get_full_name(self, local: bool) -> str:
        source = Color.fmt(f"{self.mod.source_name}", Color.MAGENTA)
        name = format_mod_name(self.mod, display_name=False)
        version = Color.fmt(self.get_version(local), Color.YELLOW)
        return f"{source}/{name}:{version}"

    def summary(self, local: bool):
        authors = Color.fmt(self.authors_list(), Color.GREEN)
        print(f"{self.get_full_name(local)} by {authors}\n    {self.mod.description}")

    def print_info(self, cache_directory: CacheDirectory):
        is_cached = cache_directory.has(self.mod, self.version)
        is_installed = self.mod.is_installed and self.mod.installation.version == self.version

        table = Table(f"Displaying information about {self.mod.display_name} in version {self.version}")
        table.add_row("Game", f"{self.mod.game.title} ({self.mod.game_id})")
        table.add_row("Source", self.mod.source_name)
        table.add_row("Name", format_mod_name(self.mod, display_name=False))
        table.add_row("Full name", self.get_full_name(local=True))
        table.add_separator()
        table.add_row("Display name", format_mod_name(self.mod))
        table.add_row("Description", self.mod.description)
        table.add_row("Is a library", self.mod.is_library, Color.YELLOW)
        table.add_row("Authors", self.authors_list(), Color.GREEN)
        table.add_row("Repository", self.mod.repository, Color.BLUE)
        table.add_row("Dependencies", ", ".join(dep.dependency.name for dep in self.mod.dependencies))
        table.add_row("Release date", self.mod.release_date.strftime(DateFormat.DETAILED))
        table.add_row("Latest version", self.mod.latest_version, Color.YELLOW)
        table.add_separator()
        table.add_row("Cached", format_bool(is_cached))
        table.add_row("Installed", format_bool(is_installed))
        if self.mod.is_installed:
            table.add_row("Installed version", self.mod.installation.version, Color.YELLOW)
        table.print()
