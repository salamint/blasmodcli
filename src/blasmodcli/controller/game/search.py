from .group import GameCommandGroup
from ...utils.cli import Argument


class Search(GameCommandGroup):
    """ Lists every mod whose name, author or description contains the given string of text. """

    terms: list[str] = Argument(nargs="*")

    def handle(self) -> int:
        raise NotImplementedError
