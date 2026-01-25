from typing import Optional

from sqlalchemy import TypeDecorator, String, Dialect


class Version:

    @classmethod
    def from_tag(cls, tag: str) -> 'Version':
        v = tag.startswith("v")
        if v:
            tag = tag[1:]
        components = tag.split(".")
        number_of_components = len(components)
        if number_of_components != 3:
            raise ValueError(f"Invalid version number: there must be exactly three components, {number_of_components} received ({tag}).")
        for i, component in enumerate(components):
            if not component.isdigit():
                raise ValueError(f"Invalid version number: component {i} is not a digit.")
        return cls(*components, v=v)

    def __init__(self, major: int, minor: int, patch: int, v: bool = False):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.v = v

    def __ge__(self, other: 'Version') -> bool:
        return self > other or self == other

    def __gt__(self, other: 'Version') -> bool:
        if self.major == other.major:
            if self.minor == other.minor:
                return self.patch > other.patch
            return self.minor > other.minor
        return self.major > other.major

    def __eq__(self, other: 'Version') -> bool:
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __le__(self, other: 'Version') -> bool:
        return self < other or self == other

    def __lt__(self, other: 'Version') -> bool:
        if self.major == other.major:
            if self.minor == other.minor:
                return self.patch < other.patch
            return self.minor < other.minor
        return self.major < other.major

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def tag(self) -> str:
        string = str(self)
        if self.v:
            return f"v{string}"
        return string


class VersionType(TypeDecorator):

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Optional[Version], dialect: Dialect) -> Optional[str]:
        if value is None:
            return None
        return value.tag

    def process_result_value(self, value: Optional[str], dialect: Dialect) -> Optional[Version]:
        if value is None:
            return None
        return Version.from_tag(value)
