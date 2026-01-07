from sqlalchemy.orm import sessionmaker, Session

from blasmodcli.repositories.game import GameRepository


class Warehouse:

    def __init__(self, session_maker: sessionmaker[Session]):
        self.session_maker = session_maker
        self.games = GameRepository(self.session_maker)
