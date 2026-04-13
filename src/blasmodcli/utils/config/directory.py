from abc import abstractmethod, ABC
from pathlib import Path
from tomllib import TOMLDecodeError
from typing import Any, Generic, TypeVar, Generator
import tomllib

from blasmodcli.exceptions.utils import ConfigurationException, MissingFieldException, InvalidFieldTypeException
from blasmodcli.utils import Directories, logger

T = TypeVar("T")


class ConfigurationDirectory(ABC, Generic[T]):

    def __init__(self, directory: Path):
        self.directory = Directories.require(directory)
        self.all: list[T] = []
        self.current_file: Path | None = None

    def get(self, data: dict[str, Any], section_name: str, field_name: str, expected_type: type) -> Any:
        try:
            value = data[field_name]
            if not isinstance(value, expected_type):
                raise InvalidFieldTypeException(self.current_file, section_name, field_name, expected_type, type(value))
            return value
        except KeyError:
            raise MissingFieldException(self.current_file, section_name, field_name)

    def files(self) -> Generator[Path]:
        for entry in self.directory.rglob("*.toml"):
            if entry.is_file():
                yield entry

    def load_all(self):
        for file in self.files():
            try:
                self.load_file(file)
            except (ConfigurationException, TOMLDecodeError) as e:
                logger.error(e)

    def load_file(self, file: Path) -> int:
        self.current_file = file
        with file.open("rb") as file:
            data = tomllib.load(file)
            instances = self.load_data(data)
            self.all.extend(instances)
            return len(instances)

    @abstractmethod
    def load_data(self, data: dict) -> list[T]:
        pass
