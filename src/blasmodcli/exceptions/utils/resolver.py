from blasmodcli.exceptions import ApplicationException
from blasmodcli.model import Mod, Version


class DependencyResolutionException(ApplicationException):
    pass


class UnresolvableDependency(DependencyResolutionException):

    def __init__(self, mod: Mod, minimum_version: Version, maximum_version: Version):
        self.mod = mod
        self.minimum_version = minimum_version
        self.maximum_version = maximum_version

    def __str__(self) -> str:
        return (f"{self.mod.display_name}'s minimum and maximum versions required are {self.minimum_version}"
                f" and {self.maximum_version} respectively ({self.minimum_version} > {self.maximum_version}).")
