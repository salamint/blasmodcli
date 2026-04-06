from blasmodcli.controller.mod.group import ModCommandGroup
from blasmodcli.exceptions import NothingToDoException
from blasmodcli.utils import Message
from blasmodcli.utils.cli import Argument
from blasmodcli.utils.resolver import ModVersion
from blasmodcli.view import step, NumberedList, accept_or_cancel


class Uninstall(ModCommandGroup):
    """ Deletes the mod and all of its files from the game's folder. """

    recursive: bool = Argument( "-r", default=False, help="Uninstall the dependencies of this mod if they are not required by any other installed mod.")
    yes: bool = Argument("-y", default=False, help="Skip the confirmation messages (download AND install).")

    def filter_uninstalled(self):
        filtered: list[ModVersion] = []
        for mod, version in self.mod_versions:
            if mod.installation is not None:
                filtered.append(ModVersion(mod, version))
        self.mod_versions = filtered

    def filter_required(self):
        filtered: list[ModVersion] = []

        mods = [mod for mod, _ in self.mod_versions]

        for mod, version in self.mod_versions:
            ignore = False
            for dep in mod.required_by:
                if dep.mod not in mods and dep.mod.is_installed:
                    Message.debug(f"Dependency {mod.display_name} ignored because required by {dep.mod.display_name} which is installed")
                    ignore = True
            if not ignore:
                filtered.append(ModVersion(mod, version))
        self.mod_versions = filtered

    @step("Installing mods...")
    def uninstall_mods(self):
        numbered_list = NumberedList(len(self.mod_versions))
        for mod, _ in self.mod_versions:
            progress = numbered_list.add_progress(f"Uninstalling {mod.display_name}...")
            mod.installation.delete()
            progress.success()

    async def handle(self) -> int:
        if self.recursive:
            exit_code = self.resolve_dependencies()
            if exit_code:
                return exit_code

        self.filter_uninstalled()
        self.filter_required()

        number_of_mods = len(self.mod_versions)

        if number_of_mods == 0:
            raise NothingToDoException("The mod and its dependencies are already installed.")

        self.print_mod_list("uninstall")
        if not self.yes:
            accept_or_cancel(f"Are you sure you want to uninstall {number_of_mods} mods?")

        self.uninstall_mods()
        Message.success(f"Successfully uninstalled {number_of_mods} mods!")
        return 0
