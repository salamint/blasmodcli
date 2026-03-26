from pathlib import Path

from blasmodcli.model import Game, ModdingTools, ModdingToolsDependency
from blasmodcli.repositories import GameRepository
from blasmodcli.utils.config.directory import ConfigurationDirectory


class GameConfiguration(ConfigurationDirectory[Game]):

    def __init__(self, directory: Path, repository: GameRepository):
        super().__init__(directory)
        self.repository = repository
        self.games: dict[str, Game] = {}

    def load_data(self, data: dict) -> list[Game]:
        games = []
        for key, attrs in data.items():
            tools_attrs = attrs.pop("tools")
            tools_dependencies = tools_attrs.pop("dependencies", {})
            tools = ModdingTools(**tools_attrs)
            for name, display_name in tools_dependencies.items():
                ModdingToolsDependency(modding_tools=tools, name=name, display_name=display_name)
            game = Game(id=key, **attrs, modding_tools=tools)
            game = self.repository.update(game)
            self.games[key] = game
            games.append(game)
        return games
