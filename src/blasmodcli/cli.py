from argparse import ArgumentParser
from enum import StrEnum
from pathlib import Path
from typing import Callable, Dict, Sequence, Union

from blasmodcli.exceptions import CancelException, DoneException
from blasmodcli.games import Game
from blasmodcli.mod import ModState
from blasmodcli.utils import Message


Handler = Union[Callable[[], int], Callable[[...], int]]


class UnusedDependenciesAction(StrEnum):
    NOTHING = "nothing"
    DEACTIVATE = "deactivate"
    UNINSTALL = "uninstall"


class CommandLineInterface:

    def __init__(self, game: 'Game'):
        self.game = game
        self.argument_parser = ArgumentParser(self.game.tool_name)
        self.subparsers = self.argument_parser.add_subparsers(dest="handler")
        self.handlers: 'Dict[str, Handler]' = {}

    def add_handler(self, handler: 'Handler', help_: str) -> ArgumentParser:
        name = handler.__name__
        if name.startswith("handle_"):
            name = name.replace("handle_", "")
        subparser = self.subparsers.add_parser(name, help=help_)
        subparser.handler = handler
        self.handlers[name] = handler
        return subparser

    def add_all_handlers(self):
        self.add_activate_handler()
        self.add_backup_handler()
        self.add_clear_handler()
        self.add_configure_handler()
        self.add_deactivate_handler()
        self.add_info_handler()
        self.add_install_handler()
        self.add_list_handler()
        self.add_search_handler()
        self.add_uninstall_handler()
        self.add_update_handler()
        self.add_upgrade_handler()

    def add_activate_handler(self):
        activate_cmd = self.add_handler(
            self.handle_activate,
            "Extracts the contents of the mod inside the Modding folder, thus activating it."
        )
        activate_cmd.add_argument("mod_name", help="Name of the mod to activate.")
        activate_cmd.add_argument(
            "--reactivate", "-r",
            help="If the mod is already activated, reactivates it. Can be used for debugging or trying to fix collision issues."
        )
        activate_cmd.add_argument(
            "--not-recursive", "-n",
            action="store_false",
            dest="recursive",
            help="Does not activate mods that this mod depends on."
        )

    def add_backup_handler(self):
        backup_cmd = self.add_handler(self.handle_backup, "Backs up your saves into an archive and exports them.")
        backup_cmd.add_argument("--destination", "-d", default=Path.cwd(), type=Path, help="")

    def add_clear_handler(self):
        clear_cmd = self.add_handler(
            self.handle_clear,
            "Deletes the 'Modding' directory that contains all activated mod. In other words, deactivate all mods in a cleaner way."
        )
        clear_cmd.add_argument(
            "--force", "-f",
            action="store_true",
            help="Skips confirmation message and straight up deletes the directory."
        )

    def add_configure_handler(self):
        self.add_handler(
            self.handle_configure,
            "Downloads and extract the modding tools for Blasphemous inside the game's folder."
        )

    def add_deactivate_handler(self):
        deactivate_cmd = self.add_handler(
            self.handle_deactivate,
            "Removes the dynamic library file associated with the mod inside the Modding folder, thus deactivating it."
        )
        deactivate_cmd.add_argument("mod_name", help="Name of the mod to deactivate.")
        deactivate_cmd.add_argument(
            "--not-recursive", "-n",
            action="store_false",
            dest="recursive",
            help="Does not deactivate mods that were only depended on by this mod."
        )

    def add_info_handler(self):
        info_cmd = self.add_handler(self.handle_info, "Displays information about a mod using its name.")
        info_cmd.add_argument("mod_name", help="Name of the mod to look up.")

    def add_install_handler(self):
        install_cmd = self.add_handler(
            self.handle_install,
            "Downloads a mod and does not activate it immediately."
        )
        install_cmd.add_argument("mod_name", help="Name of the mod to install.")
        install_cmd.add_argument(
            "--force", "-f",
            action="store_true",
            help="If the mod is already installed, overwrites the previous installation."
        )
        install_cmd.add_argument(
            "--do-not-activate", "-d",
            action="store_false",
            dest="activate_after",
            help="Whether to activate the mod after the installation or not."
        )

    def add_list_handler(self):
        list_cmd = self.add_handler(
            self.handle_list,
            "Shows the list of every mod available (or installed, or activated)."
        )
        list_cmd.add_argument(
            "--installed", "-i",
            action="store_const",
            const=ModState.INSTALLED,
            default=ModState.NONE,
            dest="state"
        )
        list_cmd.add_argument(
            "--activated", "-a",
            action="store_const",
            const=ModState.ACTIVATED,
            default=ModState.NONE,
            dest="state"
        )

    def add_search_handler(self):
        search_cmd = self.add_handler(
            self.handle_search,
            "Lists every mod whose name, author or description contains the given string of text."
        )
        search_cmd.add_argument("terms", nargs="*")

    def add_uninstall_handler(self):
        uninstall_cmd = self.add_handler(
            self.handle_uninstall,
            "Deletes the mod and all of its files from the game's folder."
        )
        uninstall_cmd.add_argument("mod_name", help="Name of the mod uninstall.")
        uninstall_cmd.add_argument(
            "--unused-dependencies-action", "--unused-deps", "-u",
            choices=[act.value for act in UnusedDependenciesAction],
            default=UnusedDependenciesAction.DEACTIVATE
        )

    def add_update_handler(self):
        self.add_handler(
            self.handle_update,
            "Updates the mod database and fetches the latest mod version, allowing to detect upgradable mods."
        )

    def add_upgrade_handler(self):
        self.add_handler(
            self.handle_upgrade,
            "Upgrades all mods (or the given one) to their latest version."
        )

    # Handlers

    def handle_activate(self, mod_name: str, reactivate: bool = False, recursive: bool = True) -> int:
        self.game.load_mods()
        mod = self.game.get_mod(mod_name)
        return mod.activate(reactivate, recursive)

    def handle_backup(self, destination: Path | None = None) -> int:
        return self.game.backup_saves(destination)

    def handle_clear(self, force: bool = False) -> int:
        return self.game.clear_modding_directory(force)

    def handle_configure(self):
        return self.game.configure_modding_tools()

    def handle_deactivate(self, mod_name: str, recursive: bool = True) -> int:
        self.game.load_mods()
        mod = self.game.get_mod(mod_name)
        return mod.deactivate(recursive)

    def handle_install(self, mod_name: str, activate_after: bool = True, force: bool = False) -> int:
        self.game.load_mods()
        mod = self.game.get_mod(mod_name)
        return mod.install(activate_after, force)

    def handle_info(self, mod_name: str) -> int:
        self.game.load_mods()
        mod = self.game.get_mod(mod_name)
        mod.print_info()
        return 0

    def handle_list(self, state: 'ModState' = ModState.NONE) -> int:
        self.game.load_mods()
        for mod in self.game.list_mods(state):
            mod.print(state is not ModState.NONE)
        return 0

    def handle_search(self, terms: list[str]) -> int:
        self.game.load_mods()
        for mod in self.game.search(terms):
            mod.print(local=False)
        return 0

    # TODO: handle uninstall
    def handle_uninstall(self, mod_name: str,
                         unused_dependencies_action: 'UnusedDependenciesAction' = UnusedDependenciesAction.DEACTIVATE) -> int:
        return 0

    def handle_update(self) -> int:
        self.game.fetch_latest_modding_tools_version()
        self.game.update_database()
        return 0

    # TODO: handle upgrade
    def handle_upgrade(self) -> int:
        return 0

    def parse_args(self, args: Sequence[str] | None = None) -> int:
        ns = self.argument_parser.parse_args(args)
        if not ns.handler:
            self.argument_parser.print_help()
            return 0
        args = ns.__dict__.copy()
        handler = args.pop("handler")
        return self.run_handler(handler, args)

    def run_handler(self, name: str, args: dict) -> int:
        try:
            return self.handlers[name](**args)
        except DoneException as e:
            Message.success(str(e))
            return 0
        except CancelException as e:
            Message.error(str(e))
            return 0
        except Exception as e:
            Message.error(f"{e.__class__.__name__}: {e}")
            return 1
