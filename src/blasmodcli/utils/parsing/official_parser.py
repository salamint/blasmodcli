from datetime import datetime
from requests import get as request
from typing import Any, Dict, Generator

from blasmodcli.model import Authorship, Mod, ModSource
from blasmodcli.utils.parsing.parser import ModListParser, ModParser
from blasmodcli.view import DateFormat

Object = Dict[str, Any]

AUTHORS_SEPARATOR = " && "


def fetch_latest_version(repository: str) -> str:
    response = request(f"{repository}/releases/latest")
    response.raise_for_status()
    return response.url.split("/")[-1]


def parse_authors(string: str) -> Generator[str]:
    with_separators = string.replace(", ", AUTHORS_SEPARATOR).replace(", && ", AUTHORS_SEPARATOR)
    for name in with_separators.split(AUTHORS_SEPARATOR):
        yield name.strip()


class OfficialModParser(ModParser):
    __parser_name__ = "official"

    def __init__(self, list_parser: 'ModListParser', data: Object):
        super().__init__(list_parser)
        self.data = data

    def get_name(self) -> str:
        return self.data["Name"]

    def parse_mod(self) -> Mod:
        repository = f"https://github.com/{self.data['GithubAuthor']}/{self.data['GithubRepo']}"
        mod = Mod(
            game_id=self.list_parser.source.game.id,
            source_name=self.list_parser.source.name,
            name=self.get_name(),
            description=self.data["Description"],
            release_date=datetime.strptime(self.data["InitialReleaseDate"], DateFormat.SIMPLE).date(),
            repository=repository,
            plugin_file_name=self.data["PluginFile"],
            version=fetch_latest_version(repository)
        )
        for author in parse_authors(self.data["Author"]):
            mod.authors.append(Authorship(mod=mod, name=author))
        return mod

    def parse_dependencies(self) -> list[str]:
        return self.data.get("Dependencies", [])


class OfficialModListParser(ModListParser):

    def __init__(self, source: ModSource):
        super().__init__(source)
        self.index = 0
        self.data: list[Object] = []

    def __next__(self) -> 'ModParser':
        if self.index < self.count():
            data = self.data[self.index]
            if not isinstance(data, dict):
                raise TypeError(f"The value at index {self.index} is of type {type(data)} and not an object.")
            self.index += 1
            return OfficialModParser(self, data)
        raise StopIteration

    def count(self) -> int:
        return len(self.data)

    def fetch(self):
        response = request(self.source.url)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            raise TypeError(f"The JSON file's contents should be a list of objects, got '{type(self.data)}' instead.")
        self.data = data
