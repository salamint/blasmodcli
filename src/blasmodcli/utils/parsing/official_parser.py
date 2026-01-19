import json
from datetime import datetime

from aiohttp import ClientSession
from typing import Any, Dict, Generator

from blasmodcli.model import Authorship, Mod, ModSource
from blasmodcli.utils.parsing.parser import ModListParser
from blasmodcli.view import DateFormat

Object = Dict[str, Any]

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
        self.data: list[Object] = []

    async def fetch(self):
        async with ClientSession() as session:
            async with session.get(self.source.url) as response:
                response.raise_for_status()
                content = await response.content.read()
        data = json.loads(content)
        if not isinstance(data, list):
            raise TypeError(f"The JSON file's contents should be a list of objects, got '{type(self.data)}' instead.")
        self.data = data
        self.total = len(self.data)

    async def parse(self):
        async with ClientSession() as session:
            await self.parse_all_mods(session)

    async def parse_all_mods(self, session: ClientSession):
        for i, data in enumerate(self.data):
            if not isinstance(data, dict):
                raise TypeError(f"The value at index {i} is of type {type(data)} and not an object.")
            await self.parse_mod(session, data)

    async def parse_mod(self, session: ClientSession, data: Object):
        repository = f"https://github.com/{data['GithubAuthor']}/{data['GithubRepo']}"
        mod = Mod(
            game_id=self.source.game.id,
            source_name=self.source.name,
            name=data["Name"],
            description=data["Description"],
            release_date=datetime.strptime(data["InitialReleaseDate"], DateFormat.SIMPLE).date(),
            repository=repository,
            plugin_file_name=data["PluginFile"],
            version=fetch_latest_version(session, repository)
        )
        for author in parse_authors(data["Author"]):
            mod.authors.append(Authorship(mod=mod, name=author))
        return mod
