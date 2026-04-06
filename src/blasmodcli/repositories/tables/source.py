from sqlalchemy.orm import Session

from blasmodcli.model import Source, Game
from blasmodcli.repositories.tables.table import TableRepository


class ModSourceRepository(TableRepository):

    def __init__(self, session: Session):
        super().__init__(session, Source)

    def get_all_by_game(self, game: Game) -> list[type[Source]]:
        return self.session.query(Source).filter(Source.game_id == game.id).all()

    def get_by_name(self, game: Game, name: str) -> type[Source] | None:
        return self.session.query(Source).filter(
            Source.game_id == game.id,
            Source.name == name
        ).one_or_none()

    def update_all(self, sources: list[Source]):
        for source in sources:
            self.update(source)

    def update(self, source: Source):
        query = self.session.query(Source).filter(
            Source.game_id == source.game_id,
            Source.name == source.name
        )
        in_db = query.one_or_none()
        if in_db is None:
            self.session.add(source)
        self.session.commit()
