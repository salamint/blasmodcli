from argparse import ArgumentParser

from sqlalchemy import create_engine

from blasmodcli.model import Base
from blasmodcli.repositories import Warehouse

from blasmodcli.utils import Directories
from blasmodcli.utils.cli import CommandLineInterface
from blasmodcli.utils.config import Configuration

APP_NAME = "blasmodcli"


class Application:

    def __init__(self):
        self.directories = Directories(APP_NAME)
        self.database_file = Directories.require(self.directories.data / "database.sqlite3", parent=True)
        self.engine = create_engine(f"sqlite:///{self.database_file.absolute()}")
        self.warehouse = Warehouse(self.engine)
        self.config = Configuration(self.directories.config, self.warehouse)

        # Initializing the database and updating the games first
        Base.metadata.create_all(self.engine)
        self.config.games.load_all()

        # Then create the argument parser and give it its arguments
        self.parser = ArgumentParser()
        self.add_parser_arguments()

        # Finally create the CLI
        self.cli = CommandLineInterface(self.config, self.directories, self.warehouse)
        self.add_command_handlers()

    def add_parser_arguments(self):
        self.parser.add_argument(
            "game",
            choices=self.warehouse.games.get_all_ids(),
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
        exit_code = self.cli.parse_args(
            self.warehouse.games.get_by_id(namespace.game),
            namespace.args
        )
        self.warehouse.session.close()
        return exit_code
