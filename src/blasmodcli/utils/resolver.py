from blasmodcli.exceptions.utils import UnresolvableDependency
from blasmodcli.model import Mod, ModVersion, Version, Dependency


class ModVersionRange:

    def __init__(self, dependency: Dependency):
        self.mod = dependency.dependency
        self.minimum_version = dependency.minimum_version
        self.maximum_version = dependency.maximum_version

    @property
    def most_recent_version(self) -> Version:
        return self.maximum_version if self.maximum_version is not None else self.mod.latest_version

    def intersection(self, other: Dependency):
        if self.minimum_version is None:
            self.minimum_version = other.minimum_version
        else:
            self.minimum_version = max(self.minimum_version, other.minimum_version)

        if self.maximum_version is None:
            self.maximum_version = other.maximum_version
        else:
            self.maximum_version = min(self.maximum_version, other.maximum_version)

        if self.minimum_version > self.maximum_version:
            raise UnresolvableDependency(self.mod, self.minimum_version, self.maximum_version)


class DependencyResolver:

    def __init__(self, mods: list[Mod]):
        self.mods = mods
        self.ranges: dict[int, ModVersionRange] = {}
        self.path = []

    def get_latest_versions(self) -> list[ModVersion]:
        return [
            ModVersion(version_range.mod, version_range.most_recent_version)
            for version_range in self.ranges.values()
        ]

    def resolve(self):
        queue: list[Dependency] = []
        for mod in self.mods:
            queue.extend(dep for dep in mod.dependencies)
        index = 0
        total = len(queue)
        while index < total:
            dependency = queue[index]
            for dep in dependency.dependency.dependencies:
                if dep in queue:
                    continue
                queue.append(dep)
                total += 1
            self.ranges[dependency.dependency_id] = ModVersionRange(dependency)
            index += 1
