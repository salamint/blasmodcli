from typing import Optional

from blasmodcli.controller.game.group import GameCommandGroup
from blasmodcli.utils import logger
from blasmodcli.utils.cli import Argument
from blasmodcli.view import Formatter

WILDCARD = "%"


class Search(GameCommandGroup):
    """ Lists every mod whose name, author or description contains the given string of text. """

    source: Optional[str] = Argument("-s", default=None, help="The name of the source in which you want to search.")
    terms: list[str] = Argument(nargs="*", help="The list of terms that must appear in the name or description of the mod.")

    async def handle(self) -> int:
        pattern = WILDCARD + WILDCARD.join(self.terms) + WILDCARD
        logger.debug(f"Searching for mod names or descriptions matching: {pattern}")
        formatter = Formatter(self.fs)
        for mod in self.tables.mods.search(self.game, self.source, pattern):
            formatter.summary(mod)
        return 0
