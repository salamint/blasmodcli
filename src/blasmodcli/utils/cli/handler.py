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
        for name, arg in self.arguments.items():
            try:
                value = getattr(namespace, name)
            except AttributeError:
                value = arg.default
            setattr(self, name, value)
        for name, choice in self.choices.items():
            try:
                value = getattr(namespace, name)
            except AttributeError:
                value = choice.default
            setattr(self, name, value)

    def post_init(self):
        pass

    @abstractmethod
    async def handle(self) -> int:
        raise NotImplementedError
