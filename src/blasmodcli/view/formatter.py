from pathlib import Path

from blasmodcli.model import Mod

from blasmodcli.utils.colors import Color
from blasmodcli.view.table import Table


class DateFormat:
    SIMPLE = "%Y-%m-%d"
    DETAILED = "%A, %e %B %Y"


def format_bool(boolean: bool) -> str:
    if boolean:
        return Color.fmt("Yes", Color.GREEN)
    return Color.fmt("No", Color.RED)


class Formatter:

    def __init__(self, mod: Mod):
        self.mod = mod

    def authors_list(self) -> str:
        return ", ".join(author.name for author in self.mod.authors)

    def get_version(self, local: bool):
        if local:
            if self.mod.installation is not None:
                return self.mod.installation.version
            return "unknown"
        return self.mod.version

    def summary(self, local: bool):
        source = Color.fmt(f"{self.mod.source_name}/", Color.MAGENTA)
        name = Color.fmt(self.mod.name, Color.BLUE if self.mod.is_library else Color.WHITE)
        version = Color.fmt(self.get_version(local), Color.YELLOW)
        authors = Color.fmt(self.authors_list(), Color.GREEN)
        print(f"{source}{name} {version} by {authors}\n    {self.mod.description}")

    def print_info(self, cache_directory: Path):
        is_cached = self.mod.is_cached(cache_directory)
        is_installed = self.mod.is_installed()

        table = Table()
        table.add_row("Game", f"{self.mod.game.title} ({self.mod.game_id})")
        table.add_row("Source", self.mod.source_name)
        table.add_row("Name", self.mod.name)
        table.add_row("Display name", self.mod.display_name)
        table.add_row("Description", self.mod.description)
        table.add_row("Is a library", self.mod.is_library, Color.YELLOW)
        table.add_row("Authors", self.authors_list(), Color.GREEN)
        table.add_row("Repository", self.mod.repository, Color.BLUE)
        table.add_row("Dependencies", ", ".join(dep.dependency.name for dep in self.mod.dependencies))
        table.add_row("Release date", self.mod.release_date.strftime(DateFormat.DETAILED))
        table.add_row("Latest version", self.mod.version, Color.YELLOW)
        table.add_row("Cached", format_bool(is_cached))
        table.add_row("Installed", format_bool(is_installed))
        if is_cached:
            table.add_row("Cached version", self.mod.get_latest_cached_version(cache_directory), Color.YELLOW)
        if is_installed:
            table.add_row("Installed version", self.mod.installation.version, Color.YELLOW)
        table.print()
