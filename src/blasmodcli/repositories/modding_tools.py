from blasmodcli.model import ModdingTools
from blasmodcli.repositories.repository import Repository


class ModdingToolsRepository(Repository):

    def update(self, modding_tools: ModdingTools) -> ModdingTools:
        query = self.session.query(ModdingTools).filter(ModdingTools.game_id == modding_tools.game_id)
        in_db = query.one_or_none()
        if in_db is not None:
            query.update({
                "mod_loader": modding_tools.mod_loader,
                "format": modding_tools.format,
                "url": modding_tools.url,
                "author": modding_tools.author,
            })
        else:
            self.session.add(modding_tools)
            in_db = modding_tools
        self.session.commit()
        return in_db
