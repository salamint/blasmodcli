from pathlib import Path

from blasmodcli.model import Source
from blasmodcli.repositories import ModSourceRepository
from blasmodcli.utils.config.directory import ConfigurationDirectory


class SourceConfiguration(ConfigurationDirectory[Source]):

    def __init__(self, directory: Path, repository: ModSourceRepository):
        super().__init__(directory)
        self.repository = repository

    def load_data(self, data: dict) -> list[Source]:
        sources = []
        for source_name, games in data.items():
            for game_id, attrs in games.items():
                section = f"{source_name}.{game_id}"
                source = Source(
                    game_id=game_id,
                    name=source_name,
                    format=self.get(attrs, section, "format", str),
                    url=self.get(attrs, section, "url", str),
                    maintainer=self.get(attrs, section, "maintainer", str),
                )
                sources.append(source)
        return sources
