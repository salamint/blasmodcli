from sqlalchemy.orm import sessionmaker, Session


class Repository:

    def __init__(self, session_maker: sessionmaker[Session]):
        self.session = session_maker
