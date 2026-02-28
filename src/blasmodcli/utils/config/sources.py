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
                source = Source(
                    game_id=game_id,
                    name=source_name,
                    format=attrs["format"],
                    url=attrs["url"],
                    maintainer=attrs["maintainer"],
                )
                sources.append(source)
        return sources
