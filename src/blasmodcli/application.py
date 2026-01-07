from argparse import ArgumentParser

from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker

from blasmodcli.model import Base, Game
from blasmodcli.repositories import Warehouse

from blasmodcli.utils import Directories, Message
from blasmodcli.utils.cli import CommandLineInterface

APP_NAME = "blasmodcli"


class Application:

    def __init__(self):
        self.cli = CommandLineInterface()
        self.parser = ArgumentParser()
        self.directories = Directories(APP_NAME)

        self.database_file = Directories.require(self.directories.data / "database.sqlite3", parent=True)
        self.engine = create_engine(f"sqlite:///{self.database_file.absolute()}")
        self.session_maker = sessionmaker(self.engine)
        self.repositories = Warehouse(self.session_maker)

        Base.metadata.create_all(self.engine)
        self.add_parser_arguments()
        self.add_command_handlers()

    def add_parser_arguments(self):
        self.parser.add_argument(
            "game",
            choices=self.repositories.games.get_all_names(),
            help="Name of the game on which to operate.",
            type=str
        )
        self.parser.add_argument(
            "args",
            help="Arguments to pass to the handler.",
            nargs='*'
        )

    def add_command_handlers(self):
        pass

    def run(self) -> int:
        namespace = self.parser.parse_args()
        game = select(Game).where()
        if game is not None:
            return self.cli.parse_args(namespace.args)
        Message.error("No game selected")
        return 1
