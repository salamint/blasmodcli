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
            modding_tools = self.load_modding_tools(attrs["tools"])
            game = Game(
                id=key,
                title=attrs["title"],
                steamapp_id=attrs["steamapp_id"],
                developer=attrs["developer"],
                publisher=attrs["publisher"],
                linux_native=attrs["linux_native"],
                saves_directory=attrs["saves_directory"],
                modding_tools=modding_tools
            )
            game = self.repository.update(game)
            self.games[key] = game
            games.append(game)
        return games

    def load_modding_tools(self, data: dict) -> ModdingTools:
        modding_tools = ModdingTools(
            mod_loader=data["mod_loader"],
            format=data["format"],
            url=data["url"],
            author=data["author"],
            script_filename=data.get("script_filename"),
        )
        dependencies = data.pop("dependencies", {})
        for name, display_name in dependencies.items():
            ModdingToolsDependency(
                modding_tools=modding_tools,
                name=name,
                display_name=display_name
            )
        return modding_tools
