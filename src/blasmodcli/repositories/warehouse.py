from sqlalchemy import Engine
from sqlalchemy.orm import Session

from blasmodcli.repositories.dependency import DependencyRepository
from blasmodcli.repositories.game import GameRepository
from blasmodcli.repositories.mod import ModRepository
from blasmodcli.repositories.mod_source import ModSourceRepository


class TableRepositories:

    def __init__(self, engine: Engine):
        self.session = Session(engine, autoflush=False)
        self.dependencies = DependencyRepository(self.session)
        self.games = GameRepository(self.session)
        self.mods = ModRepository(self.session)
        self.sources = ModSourceRepository(self.session)

    def commit(self):
        self.session.commit()
