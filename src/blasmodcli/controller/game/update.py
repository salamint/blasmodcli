from .group import GameCommandGroup


class Update(GameCommandGroup):
    """ Updates the mod database and fetches the latest mod version, allowing to detect upgradable mods. """

    def handle(self) -> int:
        raise NotImplementedError
