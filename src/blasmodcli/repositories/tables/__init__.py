from sqlalchemy import Engine
from sqlalchemy.orm import Session

from .dependency import DependencyRepository
from .game import GameRepository
from .mod import ModRepository
from .source import ModSourceRepository


class TableRepositories:

    def __init__(self, engine: Engine):
        self.session = Session(engine, autoflush=False)
        self.dependencies = DependencyRepository(self.session)
        self.games = GameRepository(self.session)
        self.mods = ModRepository(self.session)
        self.sources = ModSourceRepository(self.session)

    def commit(self):
        self.session.commit()
