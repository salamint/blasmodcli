from abc import ABC, abstractmethod
from pathlib import Path

from blasmodcli.exceptions.base import ApplicationException


class ConfigurationException(ApplicationException):
    pass


class TOMLSectionException(ConfigurationException, ABC):

    def __init__(self, config_file: Path, section_name: str):
        self.config_file = config_file
        self.section_name = section_name

    @abstractmethod
    def __str__(self) -> str:
        pass


class TOMLFieldException(TOMLSectionException, ABC):

    def __init__(self, config_file: Path, section_name: str, field_name: str):
        super().__init__(config_file, section_name)
        self.field_name = field_name

    @abstractmethod
    def __str__(self) -> str:
        pass


class MissingSectionException(TOMLSectionException):

    def __str__(self) -> str:
        return f"Missing section '[{self.section_name}]' in configuration file '{self.config_file}'."


class MissingFieldException(TOMLFieldException):

    def __str__(self) -> str:
        return (
            f"Missing field '{self.field_name}' in section '[{self.section_name}]'"
            f" in configuration file '{self.config_file}'."
        )


class InvalidFieldTypeException(TOMLFieldException):

    def __init__(self, config_file: Path, section_name: str, field_name: str, expected_type: type, received_type: type):
        super().__init__(config_file, section_name, field_name)
        self.expected_type = expected_type
        self.received_type = received_type

    def __str__(self) -> str:
        return (
            f"Invalid type '{self.received_type.__name__}' for field '{self.field_name}' of type expected type"
            f" '{self.expected_type.__name__}' in section '[{self.section_name}]'"
            f" in configuration file '{self.config_file}'."
        )
