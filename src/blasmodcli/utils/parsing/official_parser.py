import json
from datetime import datetime

from aiohttp import ClientSession
from typing import Generator

from blasmodcli.model import Authorship, Mod, ModSource
from blasmodcli.utils.parsing.parser import ModListParser, Object
from blasmodcli.view import DateFormat

AUTHORS_SEPARATOR = " && "


async def fetch_latest_version(session: ClientSession, repository: str) -> str:
    url = f"{repository}/releases/latest"
    async with session.get(url) as response:
        response.raise_for_status()
        return response.url.path


def parse_authors(string: str) -> Generator[str]:
    with_separators = string.replace(", ", AUTHORS_SEPARATOR).replace(", && ", AUTHORS_SEPARATOR)
    for name in with_separators.split(AUTHORS_SEPARATOR):
        yield name.strip()


class OfficialModListParser(ModListParser):
    __parser_name__ = "official"

    def __init__(self, source: ModSource):
        super().__init__(source)
        self.all_data: list[Object] = []

    async def fetch(self):
        async with ClientSession() as session:
            async with session.get(self.source.url) as response:
                response.raise_for_status()
                content = await response.content.read()
        data = json.loads(content)
        if not isinstance(data, list):
            raise TypeError(f"The JSON file's contents should be a list of objects, got '{type(self.all_data)}' instead.")
        self.all_data = data
        self.total = len(self.all_data)

    def data(self) -> Generator[Object]:
        for i, data in enumerate(self.all_data):
            if not isinstance(data, dict):
                raise TypeError(f"The value at index {i} is of type {type(data)} and not an object.")
            yield data

    async def parse(self, data: Object) -> Mod:
        repository = f"https://github.com/{data['GithubAuthor']}/{data['GithubRepo']}"
        async with ClientSession() as session:
            version = await fetch_latest_version(session, repository)
        mod = Mod(
            game_id=self.source.game_id,
            source_name=self.source.name,
            name=data["Name"],
            description=data["Description"],
            release_date=datetime.strptime(data["InitialReleaseDate"], DateFormat.SIMPLE).date(),
            repository=repository,
            plugin_file_name=data["PluginFile"],
            version=version
        )
        for author in parse_authors(data["Author"]):
            mod.authors.append(Authorship(mod=mod, name=author))
        return mod
