from abc import ABC, abstractmethod
from argparse import Namespace

from blasmodcli.model import Game
from blasmodcli.utils.cli.context import CommandContext
from blasmodcli.utils.cli.meta_handler import MetaCommandHandler


class CommandHandler(ABC, metaclass=MetaCommandHandler):

    def __init__(self, context: CommandContext, game: Game, namespace: Namespace):
        self.config = context.config
        self.directories = context.directories
        self.warehouse = context.warehouse
        self.game = game
        for arg in self.arguments:
            setattr(self, arg, getattr(namespace, arg))
        self.post_init()

    def post_init(self):
        pass

    @abstractmethod
    async def handle(self) -> int:
        raise NotImplementedError
