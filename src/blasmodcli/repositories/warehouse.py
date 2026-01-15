from sqlalchemy.orm import sessionmaker, Session

from blasmodcli.repositories.game import GameRepository
from blasmodcli.repositories.mod import ModRepository
from blasmodcli.repositories.mod_source import ModSourceRepository


class Warehouse:

    def __init__(self, session_maker: sessionmaker[Session]):
        self.session_maker = session_maker
        self.games = GameRepository(self.session_maker)
        self.mods = ModRepository(self.session_maker)
        self.mod_sources = ModSourceRepository(self.session_maker)
