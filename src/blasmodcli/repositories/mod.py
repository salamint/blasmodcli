from typing import Optional

from sqlalchemy import desc, or_, Row
from sqlalchemy.sql.operators import and_

from blasmodcli.model import ModSource, Mod, Game, ModState, ModInstallation, Version
from blasmodcli.repositories.repository import Repository
from blasmodcli.utils.caching import CacheDirectory


class ModRepository(Repository):

    def add_all(self, mods: list[Mod]):
        self.session.add_all(mods)
        self.session.commit()

    def get_all(self, game: Game, cache_directory: CacheDirectory, state: ModState = ModState.NONE) -> list[type[Mod]]:
        mods: list[type[Mod]] = []
        results:list[type[Mod]] = self.session.query(Mod).filter(
            Mod.game_id == game.id
        ).order_by(
            Mod.source_name,
            desc(Mod.is_library),
            Mod.name
        ).all()
        for mod in results:
            is_none = state is ModState.NONE
            is_cached = state is ModState.CACHED and cache_directory.has(mod)
            is_installed = state is ModState.INSTALLED and mod.is_installed
            if is_none or is_cached or is_installed:
                mods.append(mod)
        return mods

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

    def get_upgrades(self, game: Game) -> list[type[Mod]]:
        return self.session.query(Mod).filter(
            and_(
                and_(
                    Mod.game_id == game.id,
                    Mod.id == ModInstallation.mod_id,
                    ),
                Mod.latest_version != ModInstallation.version
            )
        ).all()

    def search(self, game: Game, source: Optional[str], pattern: str) -> list[type[Mod]]:
        query = self.session.query(Mod).filter(
            Mod.game_id == game.id
        ).filter(or_(
            Mod.name.ilike(pattern),
            Mod.description.ilike(pattern)
        ))
        if source is not None:
            query = query.filter(Mod.source_name == source)
        return query.order_by(Mod.source_name, desc(Mod.is_library), Mod.name).all()

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
