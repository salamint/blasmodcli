from abc import ABC, abstractmethod
from typing import Any, Dict, Generator

from blasmodcli.model import Mod, ModSource, Dependency
from blasmodcli.utils.parsing.meta_parser import MetaModListParser

Object = Dict[str, Any]


class ModListParser(ABC, metaclass=MetaModListParser):

    def __init__(self, source: ModSource):
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

    @abstractmethod
    async def parse(self, data: Object):
        pass

    async def parse_all(self):
        for data in self.data():
            await self.parse(data)

    async def parse_mod(self, data: Object):
        mod = await self.parse(data)
        self.mods[mod.name] = mod

    def resolve_dependencies(self):
        for mod_name, dependencies in self.dependencies.items():
            mod = self.mods[mod_name]
            for dependency_name in dependencies:
                dependency = self.mods[dependency_name]
                mod.dependencies.append(Dependency(mod=mod, dependency=dependency))
