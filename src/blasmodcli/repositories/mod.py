from typing import Optional

from sqlalchemy import or_

from blasmodcli.model import ModSource, Mod, Game
from blasmodcli.repositories.repository import Repository


class ModRepository(Repository):

    def add_all(self, mods: list[Mod]):
        self.session.add_all(mods)
        self.session.commit()

    def get_all_by_name(self, game: Game, name: str) -> list[type[Mod]]:
        return self.session.query(Mod).filter(
            Mod.game_id == game.id,
            Mod.name == name
        ).all()

    def get_by_name(self, source: ModSource, name: str) -> type[Mod]:
        return self.session.query(Mod).filter(
            Mod.game_id == source.game_id,
            Mod.source_name == source.name,
            Mod.name == name
        ).one()

    def search(self, game: Game, source: Optional[str], pattern: str) -> list[type[Mod]]:
        query = self.session.query(Mod).filter(
            Mod.game_id == game.id
        ).filter(or_(
            Mod.name.ilike(pattern),
            Mod.description.ilike(pattern)
        ))
        if source is not None:
            query = query.filter(Mod.source_name == source)
        return query.all()

    def update_all(self, mods: list[Mod]):
        for mod in mods:
            self.update(mod)

    def update(self, mod: Mod):
        query = self.session.query(Mod).filter(
            Mod.game_id == mod.game_id,
            Mod.source_name == mod.source_name,
            Mod.name == mod.name
        )
        in_db = query.one_or_none()
        if in_db is None:
            self.session.add(mod)
        self.session.commit()
