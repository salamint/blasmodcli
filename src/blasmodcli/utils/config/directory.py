import tomllib
from abc import abstractmethod, ABC
from pathlib import Path
from typing import Generic, TypeVar, Generator

from blasmodcli.utils import Directories

T = TypeVar("T")


class ConfigurationDirectory(ABC, Generic[T]):

    def __init__(self, directory: Path):
        self.directory = Directories.require(directory)
        self.all: list[T] = []

    def files(self) -> Generator[Path]:
        for entry in self.directory.rglob("*.toml"):
            if entry.is_file():
                yield entry

    def load_all(self):
        for file in self.files():
            self.load_file(file)

    def load_file(self, file: Path) -> int:
        with file.open("rb") as file:
            data = tomllib.load(file)
            instances = self.load_data(data)
            self.all.extend(instances)
            return len(instances)

    @abstractmethod
    def load_data(self, data: dict) -> list[T]:
        pass
