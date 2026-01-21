from typing import Optional

from sqlalchemy import or_

from blasmodcli.model import ModSource, Mod, Game
from blasmodcli.repositories.repository import Repository


class ModRepository(Repository):

    def add_all(self, mods: list[Mod]):
        with self.session() as session:
            session.add_all(mods)
            session.commit()

    def get_all_by_name(self, game: Game, name: str) -> list[type[Mod]]:
        with self.session() as session:
            return session.query(Mod).filter_by(
                game_id=game.id,
                name=name
            ).all()

    def get_by_name(self, source: ModSource, name: str) -> type[Mod]:
        with self.session() as session:
            return session.query(Mod).filter_by(
                game_id=source.game_id,
                source_name=source.name,
                name=name
            ).one()

    def search(self, game: Game, source: Optional[str], pattern: str) -> list[type[Mod]]:
        with self.session() as session:
            query = session.query(Mod).filter_by(
                game_id=game.id
            ).filter(or_(
                Mod.name.ilike(pattern),
                Mod.description.ilike(pattern)
            ))
            if source is not None:
                query = query.filter_by(sourc_name=source)
            return query.all()
