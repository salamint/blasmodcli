from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from blasmodcli.model.base import Base


class Version(Base):
    __tablename__ = "version"
    __table_args__ = (
        UniqueConstraint("major", "minor", "patch", name="unique_version"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    major: Mapped[int]
    minor: Mapped[int]
    patch: Mapped[int]

    @classmethod
    def from_string(cls, string: str) -> 'Version':
        components = string.replace("v", "").split(".")
        number_of_components = len(components)
        if number_of_components != 3:
            raise ValueError(f"Invalid version number: there must be exactly three components, {number_of_components} received.")
        for i, component in enumerate(components):
            if not component.isdigit():
                raise ValueError(f"Invalid version number: component {i} is not a digit.")
        return cls(major=components[0], minor=components[1], patch=components[2])

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
