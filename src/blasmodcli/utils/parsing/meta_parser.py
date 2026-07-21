from abc import ABCMeta
from typing import Any


class MetaModListParser(ABCMeta):

    _parsers: dict[str, 'MetaModListParser'] = {}

    def __new__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        instance = super().__new__(cls, name, bases, dct)
        parser_name = dct.get("__parser_name__")
        if parser_name is not None:
            cls._parsers[parser_name] = instance
        return instance
