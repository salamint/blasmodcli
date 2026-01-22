from blasmodcli.model import ModSource, Game
from blasmodcli.repositories.repository import Repository


class ModSourceRepository(Repository):

    def get_all_by_game(self, game: Game) -> list[type[ModSource]]:
        return self.session.query(ModSource).filter(ModSource.game_id == game.id).all()

    def update_all(self, sources: list[ModSource]):
        for source in sources:
            self.update(source)

    def update(self, source: ModSource):
        query = self.session.query(ModSource).filter(
            ModSource.game_id == source.game_id,
            ModSource.name == source.name
        )
        in_db = query.one_or_none()
        if in_db is None:
            self.session.add(source)
        self.session.commit()
