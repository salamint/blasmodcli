import re
from abc import ABC

from sqlalchemy.exc import NoResultFound

from blasmodcli.exceptions import UnknownModError, MultipleModsError, UnresolvableDependency
from blasmodcli.model import Version
from blasmodcli.model.mod import Mod
from blasmodcli.utils import Message, logger
from blasmodcli.utils.cli import CommandHandler, Argument
from blasmodcli.utils.resolver import DependencyResolver, ModVersion
from blasmodcli.view import step, ModList

MOD_FULL_NAME_REGEX = re.compile(
    r"^((?P<source_name>[a-zA-Z]+[a-zA-Z0-9]*(-[a-zA-Z]+[a-zA-Z0-9]*)*)/)?"
    r"(?P<mod_name>[a-zA-Z]+[a-zA-Z0-9]*(-[a-zA-Z]+[a-zA-Z0-9]*)*)"
    r"(:(?P<tag>v?[0-9]+\.[0-9]+\.[0-9]+))?$"
)


class ModCommandGroup(CommandHandler, ABC):
    """ Regroups commands that operate on a single mod. """
    __group__ = "mod"

    mod_names: list[str] = Argument(nargs="*", help="The name(s) of the mod(s) on which to operate.")
    mod_versions: list[ModVersion]

    def get_mod_from_full_name(self, source_name: str, mod_name: str) -> Mod | None:
        source = self.tables.sources.get_by_name(self.game, source_name)
        if source is None:
            Message.error(f"Unknown source named '{source_name}'.")
            return None
        try:
            return self.tables.mods.get_by_name(source, mod_name)
        except NoResultFound:
            raise UnknownModError(self.game, mod_name)

    def get_mod_from_name_only(self, mod_name: str) -> Mod:
        mods = self.tables.mods.get_all_by_name(self.game, mod_name)
        number_of_mods = len(mods)
        if number_of_mods == 0:
            raise UnknownModError(self.game, mod_name)
        elif number_of_mods == 1:
            return mods[0]
        else:
            sources = [mod.source_name for mod in mods]
            raise MultipleModsError(self.game, mod_name, sources)

    def post_init(self) -> int:
        self.mod_versions = []
        for mod_name in self.mod_names:
            match = MOD_FULL_NAME_REGEX.match(mod_name)
            if match is None:
                Message.error(f"The mod name '{mod_name}' does not match the format '(source_name/)mod_name(:tag)'.")
                return 1

            source_name = match.group("source_name")
            mod_name = match.group("mod_name")
            tag = match.group("tag")

            if source_name is not None:
                mod = self.get_mod_from_full_name(source_name, mod_name)
            else:
                mod = self.get_mod_from_name_only(mod_name)
            version = Version.from_tag(tag) if tag is not None else mod.latest_version

            if mod is None:
                return 1
            self.mod_versions.append(ModVersion(mod, version))
        return 0

    @step("Resolving dependencies...")
    def resolve_dependencies(self):
        resolver = DependencyResolver([mv.mod for mv in self.mod_versions])
        try:
            resolver.resolve()
        except UnresolvableDependency as e:
            logger.error(str(e))
            return 1
        self.mod_versions.extend(resolver.get_latest_versions())
        return 0

    def print_mod_list(self, action: str):
        number_of_mods = len(self.mod_versions)
        mod_list = ModList(f"{number_of_mods} mods to {action}:")
        mod_list.add_mods(self.mod_versions)
        mod_list.display()
