from blasmodcli.exceptions.base import ApplicationException


class CriticalBackendException(ApplicationException):
    pass


class CommandInMultipleGroupsError(CriticalBackendException):

    def __init__(self, command_groups: list[str], command: str, base_groups: tuple[type]):
        self.command_groups = command_groups
        self.command = command
        self.base_groups = base_groups

    def get_number_of_groups(self) -> int:
        number_of_groups = 0
        for group in self.base_groups:
            if group in self.command_groups:
                number_of_groups += 1
        return number_of_groups

    def __str__(self) -> str:
        return (
            f"The '{self.command}' command cannot be part of {self.get_number_of_groups()} groups."
            f" It can only be in one group."
        )
