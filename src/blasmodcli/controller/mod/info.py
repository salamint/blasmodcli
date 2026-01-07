from blasmodcli.controller.mod.group import ModCommandGroup
from blasmodcli.view import Formatter


class Info(ModCommandGroup):
    """ Displays information about a mod using its name. """

    async def handle(self) -> int:
        formatter = Formatter(self.fs)
        for i, (mod, version) in enumerate(self.mod_versions):
            if i != 0:
                print()
            formatter.print_info(mod, version)
        return 0
