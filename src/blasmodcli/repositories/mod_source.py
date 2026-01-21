from blasmodcli.model import ModSource, Game
from blasmodcli.repositories.repository import Repository


class ModSourceRepository(Repository):

    def get_all_by_game(self, game: Game) -> list[type[ModSource]]:
        with self.session() as session:
            return session.query(ModSource).filter_by(game_id=game.id).all()

    def update(self, sources: list[ModSource]):
        with self.session() as session:
            for source in sources:
                query = session.query(ModSource).filter_by(game_id=source.game.id, name=source.name)
                in_db = query.one_or_none()
                if in_db is not None:
                    query.update({
                        "format": source.format,
                        "url": source.url,
                        "maintainer": source.maintainer,
                    })
                else:
                    session.add(source)
            session.commit()
