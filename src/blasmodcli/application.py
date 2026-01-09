from argparse import ArgumentParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blasmodcli.config import Configuration
from blasmodcli.controller import *
from blasmodcli.model import Base
from blasmodcli.repositories import Warehouse

from blasmodcli.utils import Directories
from blasmodcli.utils.cli import CommandLineInterface

APP_NAME = "blasmodcli"


class Application:

    def __init__(self):
        self.directories = Directories(APP_NAME)
        self.config = Configuration(self.directories.config)
        self.cli = CommandLineInterface()
        self.parser = ArgumentParser()

        self.database_file = Directories.require(self.directories.data / "database.sqlite3", parent=True)
        self.engine = create_engine(f"sqlite:///{self.database_file.absolute()}")
        self.session_maker = sessionmaker(self.engine)
        self.repositories = Warehouse(self.session_maker)

        Base.metadata.create_all(self.engine)
        self.config.load_games(self.repositories.games)
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
        # Game commands
        self.cli.add_handler(Backup)
        self.cli.add_handler(Configure)
        self.cli.add_handler(List)
        self.cli.add_handler(Search)
        self.cli.add_handler(Update)

        # Mod commands
        self.cli.add_handler(Activate)
        self.cli.add_handler(Deactivate)
        self.cli.add_handler(Info)
        self.cli.add_handler(Install)
        self.cli.add_handler(Uninstall)
        self.cli.add_handler(Upgrade)

    def run(self) -> int:
        namespace = self.parser.parse_args()
        return self.cli.parse_args(
            self.repositories.games.get_by_name(namespace.game),
            namespace.args
        )
