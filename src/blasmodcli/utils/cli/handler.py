from abc import ABC, abstractmethod
from argparse import Namespace

from blasmodcli.model import Game
from blasmodcli.utils.caching import CacheDirectory
from blasmodcli.utils.cli.context import CommandContext
from blasmodcli.utils.cli.meta_handler import MetaCommandHandler


class CommandHandler(ABC, metaclass=MetaCommandHandler):

    def __init__(self, context: CommandContext, game: Game, namespace: Namespace):
        self.context = context
        self.config = self.context.config
        self.directories = self.context.directories
        self.warehouse = self.context.warehouse
        self.cache = CacheDirectory(self.directories.cache)
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

    async def call(self, handler: MetaCommandHandler, **kwargs) -> int:
        namespace = Namespace(**kwargs)
        controller = handler(self.context, self.game, namespace)
        exit_code = controller.post_init()
        if exit_code:
            return exit_code
        return await controller.handle()

    @abstractmethod
    async def handle(self) -> int:
        raise NotImplementedError
