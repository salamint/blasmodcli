from abc import ABC, abstractmethod
from argparse import Namespace

from blasmodcli.model import Game
from blasmodcli.repositories import Warehouse
from blasmodcli.utils.cli.meta_handler import MetaCommandHandler


class CommandHandler(ABC, metaclass=MetaCommandHandler):

    def __init__(self, warehouse: Warehouse, game: Game, namespace: Namespace):
        self.game = game
        for arg in self.arguments:
            setattr(self, arg, getattr(namespace, arg))
        self.warehouse = warehouse
        self.post_init()

    def post_init(self):
        pass

    @abstractmethod
    def handle(self) -> int:
        raise NotImplementedError
