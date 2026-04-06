from sqlalchemy.orm import Session

from blasmodcli.model import Game
from blasmodcli.repositories.tables.modding_tools import ModdingToolsRepository
from blasmodcli.repositories.tables.table import TableRepository


class GameRepository(TableRepository):

    def __init__(self, session: Session):
        super().__init__(session, Game)
        self.modding_tools = ModdingToolsRepository(session)

    def get_by_id(self, id: str) -> type[Game]:
        return self.session.query(Game).filter(Game.id == id).one()

    def get_all_ids(self) -> list[str]:
        names = []
        for result in self.session.query(Game).all():
            names.append(result.id)
        return names

    def update(self, game: Game):
        query = self.session.query(Game).filter(Game.id == game.id)
        in_db = query.one_or_none()
        if in_db is None:
            self.session.add(game)
        self.session.commit()
