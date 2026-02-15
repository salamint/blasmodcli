from blasmodcli.controller.mod.group import ModCommandGroup
from blasmodcli.exceptions import NothingToDoException
from blasmodcli.utils import Message
from blasmodcli.utils.cli import Argument
from blasmodcli.view import NumberedList, step, accept_or_cancel


class Remove(ModCommandGroup):
    """ Removes a mod from the cache. """

    recursive: bool = Argument("-r", default=False, help="Remove from the cache the mods that this mod depends on as well.")
    yes: bool = Argument("-y", default=False, help="Skip the confirmation message.")

    def filter_uncached(self):
        filtered = []
        for mod, version in self.mod_versions:
            if self.fs.cache.has(mod, version):
                filtered.append((mod, version))
        self.mod_versions = filtered

    @step("Removing mods...")
    def remove_mods(self):
        numbered_list = NumberedList(len(self.mod_versions))
        mods_deleted = 0
        for mod, version in self.mod_versions:
            p = numbered_list.add_progress(f"Removing version {version} of {mod.display_name} from the cache...")
            self.fs.cache.remove_version(mod, version)
            p.success()
            mods_deleted += 1

        if mods_deleted != 0:
            Message.success(f"{mods_deleted} mods have been successfully removed from the cache!")

    async def handle(self) -> int:
        if self.recursive:
            self.resolve_dependencies()

        self.filter_uncached()

        number_of_mods = len(self.mod_versions)
        if number_of_mods == 0:
            raise NothingToDoException("All the specified mods and dependencies are not present in the cache.")

        self.print_mod_list("remove")

        if not self.yes:
            accept_or_cancel(f"Are you sure you want to remove {number_of_mods} mods from the cache?")

        self.remove_mods()
        return 0
