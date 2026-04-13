from pathlib import Path

from blasmodcli.exceptions.utils import MissingSectionException
from blasmodcli.model import Game, ModdingTools, ModdingToolsDependency
from blasmodcli.repositories import GameRepository
from blasmodcli.utils.config.directory import ConfigurationDirectory


MODDING_TOOLS_SECTION_NAME = "tools"


class GameConfiguration(ConfigurationDirectory[Game]):

    def __init__(self, directory: Path, repository: GameRepository):
        super().__init__(directory)
        self.repository = repository
        self.games: dict[str, Game] = {}

    def load_data(self, data: dict) -> list[Game]:
        games = []
        for section, attrs in data.items():
            modding_tools_section = f"{section}.{MODDING_TOOLS_SECTION_NAME}"
            try:
                modding_tools = self.load_modding_tools(modding_tools_section, attrs[MODDING_TOOLS_SECTION_NAME])
            except KeyError:
                raise MissingSectionException(self.current_file, modding_tools_section)
            game = Game(
                id=section,
                title=self.get(attrs, section, "title", str),
                steamapp_id=self.get(attrs, section, "steamapp_id", int),
                developer=self.get(attrs, section, "developer", str),
                publisher=self.get(attrs, section, "publisher", str),
                linux_native=self.get(attrs, section, "linux_native", bool),
                saves_directory=self.get(attrs, section, "saves_directory", str),
                modding_tools=modding_tools
            )
            game = self.repository.update(game)
            self.games[section] = game
            games.append(game)
        return games

    def load_modding_tools(self, section: str, data: dict) -> ModdingTools:
        modding_tools = ModdingTools(
            mod_loader=self.get(data, section, "mod_loader", str),
            format=self.get(data, section, "format", str),
            url=self.get(data, section, "url", str),
            author=self.get(data, section, "author", str),
            script_filename=data.get("script_filename"),
        )
        dependencies = data.pop("dependencies", {})
        for name, display_name in dependencies.items():
            ModdingToolsDependency(modding_tools=modding_tools, name=name, display_name=display_name)
        return modding_tools
