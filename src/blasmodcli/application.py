from argparse import ArgumentParser
from logging import FileHandler, StreamHandler, Formatter, DEBUG, WARNING
import sys

from sqlalchemy import create_engine

from blasmodcli.controller import *
from blasmodcli.model import Base
from blasmodcli.utils import APP_NAME, logger, Directories
from blasmodcli.utils.cli import CommandContext, CommandLineInterface
from blasmodcli.utils.message import MessageFormatter


class Application:

    def __init__(self):
        self.directories = Directories(APP_NAME)
        self.init_logger()
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

    def init_logger(self):
        file_formatter = Formatter("[%(asctime)s][%(levelname)s][%(name)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler = FileHandler(Directories.require(self.directories.state) / "main.log")
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        stream_formatter = MessageFormatter()
        stream_handler = StreamHandler(sys.stdout)
        stream_handler.setLevel(WARNING)
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        logger.setLevel(DEBUG)
        logger.info("============================ [ NEW SESSION ] ============================")

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
