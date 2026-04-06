from sqlalchemy.orm import Session

from blasmodcli.model import ModdingTools
from blasmodcli.repositories.tables.table import TableRepository


class ModdingToolsRepository(TableRepository):

    def __init__(self, session: Session):
        super().__init__(session, ModdingTools)

    def update(self, modding_tools: ModdingTools):
        query = self.session.query(ModdingTools).filter(ModdingTools.game_id == modding_tools.game_id)
        in_db = query.one_or_none()
        if in_db is None:
            self.session.add(modding_tools)
        self.session.commit()
