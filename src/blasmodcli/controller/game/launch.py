from pathlib import Path
from os import environ
from subprocess import run

from blasmodcli.controller.game.group import GameCommandGroup
from blasmodcli.exceptions import UserCancelException
from blasmodcli.utils import Directories, logger
from blasmodcli.utils.cli import Argument
from blasmodcli.view import ChoiceGUI


class Launch(GameCommandGroup):
    """ Downloads and extract the modding tools for Blasphemous inside the game's folder. """

    choice: bool = Argument("-c", default=False, help="Opens a prompts to chose whether to start the game modded or not.")
    bypass_remembered_choice: bool = Argument("-b", default=False, help="Ignores the previously remembered choice for this game.")
    command: list[str] = Argument(nargs="*", help="The Steam command to open the game.")

    tmp_file: Path

    def post_init(self):
        super().post_init()
        self.tmp_file = Directories.require(self.directories.temp) / f"{self.game.id}.choice"

    def ask_user_if_launch_modded(self) -> bool:
        try:
            gui = ChoiceGUI(self.game.title)
        except ImportError:
            logger.error("The TCL/TK library is not installed.")
            return False

        gui.mainloop()
        if gui.launch_modded is None:
            raise UserCancelException("No choice selected.")

        if gui.remember_until_next_reboot.get():
            logger.debug("Remembering until next reboot.")
            self.save_choice(gui.launch_modded)
        return gui.launch_modded

    def get_choice_start_modded(self) -> bool:
        if self.bypass_remembered_choice:
            logger.debug("Bypassing remembered choice.")
            return self.ask_user_if_launch_modded()

        remembered_choice = self.load_choice()
        if remembered_choice is None:
            return self.ask_user_if_launch_modded()

        logger.info(f"Using remembered choice: {remembered_choice}")
        return remembered_choice

    def launch_using_steam_browser_protocol(self):
        url = f"steam://run/{self.game.steamapp_id}"
        args = []
        if self.choice:
            args.append("-c")
            if self.bypass_remembered_choice:
                args.append("-b")
        if args:
            url += f"//{' '.join(args)}"

        logger.debug(f"Opening '{url}' using Steam's browser protocol...")
        process = run(["xdg-open", url])
        return process.returncode

    def launch_vanilla(self) -> int:
        process = run(self.command)
        return process.returncode

    def launch_modded(self) -> int:
        if self.game.linux_native:
            return self.launch_modded_native()
        return self.launch_modded_through_proton()

    def launch_modded_native(self) -> int:
        command = self.command.copy()
        command.insert(0, self.game.modding_tools.script)
        process = run(command)
        return process.returncode

    def launch_modded_through_proton(self) -> int:
        env = environ.copy()
        env["WINEDLLOVERRIDES"] = "version=n,b"
        process = run(self.command, env=env)
        return process.returncode

    def load_choice(self) -> bool | None:
        if not self.tmp_file.is_file():
            return None

        choice = self.tmp_file.read_text()
        if choice == "modded":
            return True
        elif choice == "vanilla":
            return False
        return None

    def save_choice(self, modded: bool):
        self.tmp_file.write_text("modded" if modded else "vanilla")

    async def handle(self) -> int:
        if len(self.command) == 0:
            return self.launch_using_steam_browser_protocol()

        if self.choice and self.get_choice_start_modded():
            logger.debug(f"Starting {self.game.title} modded.")
            return self.launch_modded()

        logger.debug(f"Starting {self.game.title} vanilla.")
        return self.launch_vanilla()
