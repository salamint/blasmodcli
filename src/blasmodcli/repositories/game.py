from blasmodcli.model import Game, Mod, ModState
from blasmodcli.repositories.repository import Repository


class GameRepository(Repository):

    def get_by_id(self, id: str) -> type[Game]:
        with self.session() as session:
            return session.query(Game).filter(Game.id == id).one()

    def get_all_ids(self) -> list[str]:
        with self.session() as session:
            names = []
            for result in session.query(Game).all():
                names.append(result.id)
            return names

    def get_mods_for(self, game: Game, state: ModState = ModState.NONE) -> list[type[Mod]]:
        with self.session() as session:
            mods: list[type[Mod]] = []
            results = session.query(Mod).filter(Mod.game_id == game.id).all()
            for mod in results:
                if mod.state() >= state:
                    mods.append(mod)
            return mods

    def update(self, game: Game):
        with self.session() as session:
            query = session.query(Game).filter(Game.id == game.id)
            in_db = query.one_or_none()
            if in_db is not None:
                query.update({
                    "mod_loader": game.mod_loader,
                    "modding_tools_url": game.modding_tools_url,
                    "linux_native": game.linux_native,
                    "saves_directory": game.saves_directory
                })
            else:
                session.add(game)
            session.commit()
