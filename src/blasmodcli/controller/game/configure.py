from .group import GameCommandGroup


class Configure(GameCommandGroup):
    """ Downloads and extract the modding tools for Blasphemous inside the game's folder. """

    def handle(self) -> int:
        raise NotImplementedError
