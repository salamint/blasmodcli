from blasmodcli.model import Mod

from blasmodcli.utils.colors import Color
from blasmodcli.view.table import Table


class DateFormat:
    SIMPLE = "%Y-%m-%d"
    DETAILED = "%A, %e %B %Y"


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
        name = Color.fmt(self.mod.name, Color.BLUE if self.mod.is_library else Color.WHITE)
        version = Color.fmt(self.get_version(local), Color.YELLOW)
        authors = Color.fmt(self.authors_list(), Color.GREEN)
        print(f"{name} {version} by {authors}\n    {self.mod.description}")

    def print_info(self):
        installed = Color.fmt("No", Color.RED)
        activated = Color.fmt("No", Color.RED)
        if self.mod.is_installed():
            installed = Color.fmt("Yes", Color.GREEN)
            if self.mod.is_activated():
                activated = Color.fmt("Yes", Color.GREEN)

        table = Table()
        table.add_row("Name", self.mod.name)
        table.add_row("Description", self.mod.description)
        table.add_row("Authors", self.authors_list(), Color.GREEN)
        table.add_row("Repository", self.mod.repository, Color.BLUE)
        table.add_row("Dependencies", ", ".join(dep.dependency.name for dep in self.mod.dependencies))
        table.add_row("Release date", self.mod.release_date.strftime(DateFormat.DETAILED))
        table.add_row("Version", self.mod.version, Color.YELLOW)
        table.add_row("Installed", installed)
        table.add_row("Activated", activated)
        table.print()
