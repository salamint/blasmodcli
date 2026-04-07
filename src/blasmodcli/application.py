from argparse import ArgumentParser

from sqlalchemy import create_engine

from blasmodcli.controller import *
from blasmodcli.model import Base

from blasmodcli.utils import Directories
from blasmodcli.utils.cli import CommandContext, CommandLineInterface

APP_NAME = "blasmodcli"


class Application:

    def __init__(self):
        self.directories = Directories(APP_NAME)
        self.database_file = Directories.require(self.directories.data / "database.sqlite3", parent=True)
        self.engine = create_engine(f"sqlite:///{self.database_file.absolute()}")
        self.context = CommandContext(self.directories, self.engine)

        # Initializing the database and updating the games first
        Base.metadata.create_all(self.engine)
        self.context.config.games.load_all()

        # Then create the argument parser and give it its arguments
        self.parser = ArgumentParser()
        self.add_parser_arguments()

        # Finally create the CLI
        self.cli = CommandLineInterface(self.context)
        self.add_command_handlers()

    def add_parser_arguments(self):
        self.parser.add_argument(
            "game",
            choices=self.context.tables.games.get_all_ids(),
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
        self.cli.add_handler(CD)
        self.cli.add_handler(Configure)
        self.cli.add_handler(Launch)
        self.cli.add_handler(List)
        self.cli.add_handler(Search)
        self.cli.add_handler(Update)

        # Mod commands
        self.cli.add_handler(Download)
        self.cli.add_handler(Info)
        self.cli.add_handler(Install)
        self.cli.add_handler(Remove)
        self.cli.add_handler(Uninstall)
        self.cli.add_handler(Upgrade)

    def run(self) -> int:
        namespace = self.parser.parse_args()
        exit_code = self.cli.parse_args(
            self.context.tables.games.get_by_id(namespace.game),
            namespace.args
        )
        self.context.tables.session.close()
        return exit_code
