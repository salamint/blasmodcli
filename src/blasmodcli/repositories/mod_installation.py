from blasmodcli.model import ModInstallation
from blasmodcli.repositories.repository import Repository


class ModInstallationRepository(Repository):

    def get_by_id_or_none(self, mod_id: int) -> ModInstallation | None:
        return self.session.query(ModInstallation).filter(
            ModInstallation.mod_id == mod_id
        ).one_or_none()

    def update(self, installation: ModInstallation):
        query = self.session.query(ModInstallation).filter(
            ModInstallation.mod_id == installation.mod_id
        )
        in_db = query.one_or_none()
        if in_db is None:
            self.session.add(installation)
        self.session.commit()

    def delete(self, installation: ModInstallation):
        self.session.query(ModInstallation).filter(
            ModInstallation.mod_id == installation.mod_id).delete()
        self.session.commit()
