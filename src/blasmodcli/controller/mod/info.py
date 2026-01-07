from .group import ModCommandGroup


class Info(ModCommandGroup):
    """ Displays information about a mod using its name. """

    def handle(self) -> int:
        raise NotImplementedError
