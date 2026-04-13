from blasmodcli.exceptions.base import ApplicationException


class ParsingException(ApplicationException):
    pass


class NameConversionError(ParsingException):

    def __init__(self, string_to_convert: str):
        self.string_to_convert = string_to_convert

    def __str__(self) -> str:
        return f"Could not convert '{self.string_to_convert}' into a valid mod name."
