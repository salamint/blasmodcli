from abc import ABC, abstractmethod
from typing import Any, Dict, Generator

from blasmodcli.model import Mod, Source, Dependency
from blasmodcli.utils.parsing.meta_parser import MetaModListParser

Object = Dict[str, Any]


class ModListParser(ABC, metaclass=MetaModListParser):

    def __init__(self, source: Source):
        self.source = source
        self.mods: dict[str, Mod] = {}
        self.dependencies: dict[str, list[str]] = {}
        self.done = 0
        self.total = 0

    def extend(self, mods: list[Mod]):
        for mod in self.mods.values():
            mods.append(mod)

    @abstractmethod
    def data(self) -> Generator[Object]:
        pass

    @abstractmethod
    async def fetch(self):
        pass

    async def parse(self, data: Object) -> Mod:
        mod = await self.parse_internal(data)
        self.mods[mod.name] = mod
        return mod

    @abstractmethod
    async def parse_internal(self, data: Object) -> Mod:
        pass

    def resolve_dependencies(self):
        for mod_name, mod_dependencies in self.dependencies.items():
            mod = self.mods[mod_name]
            for dependency_name in mod_dependencies:
                dependency = self.mods[dependency_name]
                mod.dependencies.append(Dependency(dependency=dependency))
