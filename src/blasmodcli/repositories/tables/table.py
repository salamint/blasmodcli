from sqlalchemy.orm import Session

from blasmodcli.repositories.repository import IRepository, T


class TableRepository(IRepository):

    def __init__(self, session: Session, table: type):
        self.session = session
        self.table = table

    def get_all(self) -> list[T]:
        return self.session.query(self.table).all()
