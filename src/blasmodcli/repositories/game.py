from sqlalchemy.orm import sessionmaker, Session

from blasmodcli.model import Game, Mod, ModState
from blasmodcli.repositories.modding_tools import ModdingToolsRepository
from blasmodcli.repositories.repository import Repository


class GameRepository(Repository):

    def __init__(self, session_maker: sessionmaker[Session]):
        super().__init__(session_maker)
        self.modding_tools = ModdingToolsRepository(session_maker)

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

    def update(self, game: Game) -> Game:
        with self.session() as session:
            query = session.query(Game).filter(Game.id == game.id)
            in_db = query.one_or_none()
            if in_db is not None:
                query.update({
                    "title": game.title,
                    "developer": game.developer,
                    "publisher": game.publisher,
                    "linux_native": game.linux_native,
                    "saves_directory": game.saves_directory
                })
                self.modding_tools.update(game.modding_tools)
            else:
                session.add(game)
                in_db = game
            session.commit()
            return in_db
