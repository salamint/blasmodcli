from abc import ABC, abstractmethod
from typing import Iterator

from blasmodcli.model import Mod, ModSource, Dependency
from blasmodcli.utils.parsing.meta_parser import MetaModListParser


class ModParser(ABC):

    def __init__(self, list_parser: 'ModListParser'):
        self.list_parser = list_parser

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def parse_mod(self) -> Mod:
        pass

    @abstractmethod
    def parse_dependencies(self) -> list[str]:
        pass

    def parse(self) -> Mod:
        mod = self.parse_mod()
        self.list_parser.mods[mod.name] = mod
        self.list_parser.dependencies[mod.name] = self.parse_dependencies()
        return mod


class ModListParser(ABC, metaclass=MetaModListParser):

    def __init__(self, source: ModSource):
        self.source = source
        self.mods: dict[str, Mod] = {}
        self.dependencies: dict[str, list[str]] = {}

    def __iter__(self) -> Iterator[ModParser]:
        return self

    def __len__(self) -> int:
        return self.count()

    @abstractmethod
    def __next__(self) -> 'ModParser':
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def fetch(self):
        pass

    def add_dependencies(self):
        for mod_name, dependencies in self.dependencies.items():
            mod = self.mods[mod_name]
            for dependency_name in dependencies:
                dependency = self.mods[dependency_name]
                mod.dependencies.append(Dependency(mod=mod, dependency=dependency))
