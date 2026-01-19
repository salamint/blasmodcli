from sqlalchemy import Engine
from sqlalchemy.orm import Session

from blasmodcli.repositories.game import GameRepository
from blasmodcli.repositories.mod import ModRepository
from blasmodcli.repositories.mod_source import ModSourceRepository


class Warehouse:

    def __init__(self, engine: Engine):
        self.session = Session(engine, autoflush=False)
        self.games = GameRepository(self.session)
        self.mods = ModRepository(self.session)
        self.mod_sources = ModSourceRepository(self.session)

    def commit(self):
        self.session.commit()
