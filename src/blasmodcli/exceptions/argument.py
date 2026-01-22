from blasmodcli.exceptions.base import ApplicationException
from blasmodcli.model import Game


class ArgumentValueError(ApplicationException):
    pass


class ModNameError(ArgumentValueError):

    def __init__(self, game: Game, mod_name: str):
        self.game = game
        self.mod_name = mod_name


class UnknownModError(ModNameError):

    def __str__(self) -> str:
        return f"Unknown mod '{self.mod_name}' for the game '{self.game.title}'."


class MultipleModsError(ModNameError):

    def __init__(self, game: Game, mod_name: str, sources: list[str]):
        super().__init__(game, mod_name)
        self.sources = sources

    def __str__(self) -> str:
        sources = ", ".join(self.sources)
        return (
            f"Multiple sources available for the mod '{self.mod_name}' for the game '{self.game.title}': {sources}.\n"
            f"Please rerun the same command and prepend the name of the mod with the name of the source."
        )
