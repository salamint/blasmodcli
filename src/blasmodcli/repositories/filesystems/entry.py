from re import compile

from blasmodcli.model import ModVersion, Version


FILENAME_PATTERN = compile(
    r"^(?P<game_id>[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*)"
    r"_(?P<source_name>[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*)"
    r"_(?P<mod_name>[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*)"
    r"_(?P<version>[0-9]+\.[0-9]+\.[0-9]+)\.(?P<ext>[a-zA-Z]+[a-zA-Z0-9]*)$"
)


class Entry:

    @classmethod
    def from_mod_version(cls, mod_version: ModVersion, extension: str):
        return cls(
            mod_version.mod.game_id,
            mod_version.mod.source_name,
            mod_version.mod.name,
            mod_version.version,
            extension
        )

    def __init__(
        self,
        game_id: str,
        source_name: str,
        mod_name: str,
        version: Version,
        extension: str
    ):
        self.game_id = game_id
        self.source_name = source_name
        self.mod_name = mod_name
        self.version = version
        self.extension = extension

    @property
    def filename(self):
        return f"{self.game_id}_{self.source_name}_{self.mod_name}_{self.version}.{self.extension}"
