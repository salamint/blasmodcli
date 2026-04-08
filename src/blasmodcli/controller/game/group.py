from abc import ABC

from blasmodcli.model import ModState, ModVersion
from blasmodcli.utils import logger
from blasmodcli.utils.cli import CommandHandler


class GameCommandGroup(CommandHandler, ABC):
    """ Regroups commands that operate on a single mod. """
    __group__ = "game"

    def get_mods(self, state: ModState = ModState.NONE) -> list[ModVersion]:
        precision = f" that are {state.name.lower()}" if state is not ModState.NONE else ""
        logger.debug(f"Querying all mods for {self.game.title}{precision}...")
        mod_versions = []
        match state:
            case ModState.NONE:
                for mod in self.game.mods:
                    mod_versions.append(ModVersion(mod))
            case ModState.CACHED:
                for mod_version in self.fs.cache.get_all_latest_versions(self.game):
                    mod_versions.append(mod_version)
            case ModState.INSTALLED:
                for mod_version in self.fs.installations.get_all_latest_versions(self.game):
                    mod_versions.append(mod_version)
        return mod_versions
