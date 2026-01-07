from .group import ModCommandGroup


class Upgrade(ModCommandGroup):
    """ Upgrades all mods (or the given one) to their latest version. """

    def handle(self) -> int:
        raise NotImplementedError
