from blasmodcli.model import Dependency
from blasmodcli.repositories.repository import Repository


class DependencyRepository(Repository):

    def update_all(self, dependencies: list[Dependency]):
        for dependency in dependencies:
            self.update(dependency)

    def update(self, dependency: Dependency):
        query = self.session.query(Dependency).filter(
            Dependency.mod_id == dependency.mod_id,
            Dependency.dependency_id == dependency.dependency_id
        )
        in_db = query.one_or_none()
        if in_db is None:
            self.session.add(dependency)
        self.session.commit()
