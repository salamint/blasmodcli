from blasmodcli.model import Game, Mod
from blasmodcli.repositories.repository import Repository


class GameRepository(Repository):

    def get_by_name(self, name: str) -> type[Game]:
        with self.session() as session:
            return session.query(Game).filter_by(name=name).one()

    def get_all_names(self) -> list[str]:
        with self.session() as session:
            names = []
            for result in session.query(Game).all():
                names.append(result.name)
            return names

    def get_mods_for(self, game: Game) -> list[type[Mod]]:
        with self.session() as session:
            return session.query(Mod).filter_by(game_name=game.name).all()

    def sync(self, game: Game):
        with self.session() as session:
            query = session.query(Game).filter_by(name=game.name)
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
