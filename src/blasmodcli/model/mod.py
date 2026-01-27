import re
from datetime import date
from enum import IntEnum
from pathlib import Path
from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from blasmodcli.model.base import Base
from blasmodcli.model.version import Version, VersionType


ARCHIVE_FILENAME_PATTERN = re.compile(r"^(?P<game_id>[a-z]+)-(?P<source_name>[a-z]+)-(?P<mod_name>[a-z]+)-(?P<version>[0-9]+\.[0-9]+\.[0-9]+).zip$")


class DateFormat:
    SIMPLE = "%Y-%m-%d"
    DETAILED = "%A, %e %B %Y"


class ModState(IntEnum):
    NONE = 0
    CACHED = 1
    INSTALLED = 2


class Mod(Base):
    __tablename__ = "mod"
    __table_args__ = (
        UniqueConstraint("game_id", "source_name", "name", name="unique_name_per_source_per_game"),
        UniqueConstraint("game_id", "source_name", "repository", name="unique_repository_per_source_per_game"),
        UniqueConstraint("game_id", "source_name", "plugin_file_name", name="unique_plugin_file_per_source_per_game"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    game_id: Mapped[str] = mapped_column(ForeignKey("game.id"))
    game: Mapped['Game'] = relationship("Game")

    source_name: Mapped[str] = mapped_column(ForeignKey("mod_source.name"))
    source: Mapped['ModSource'] = relationship("ModSource", back_populates="mods")

    name: Mapped[str]
    display_name: Mapped[str]
    description: Mapped[str]
    is_library: Mapped[bool]
    release_date: Mapped[date]
    repository: Mapped[str]
    version: Mapped['Version'] = mapped_column(VersionType)
    plugin_file_name: Mapped[str]

    dependencies: Mapped[List['Dependency']] = relationship(
        "Dependency",
        back_populates="mod",
        foreign_keys="Dependency.mod_id",
        cascade="all, delete-orphan"
    )

    required_by: Mapped[List['Dependency']] = relationship(
        "Dependency",
        back_populates="dependency",
        foreign_keys="Dependency.dependency_id",
        cascade="all, delete-orphan"
    )

    authors: Mapped[List['Authorship']] = relationship("Authorship", back_populates="mod")

    installation: Mapped[Optional['ModInstallation']] = relationship("ModInstallation", back_populates="mod")

    @property
    def archive_name(self) -> str:
        return f"{self.game_id}-{self.source_name}-{self.name}-{self.version}.zip"

    @property
    def full_name(self):
        return f"{self.source.name}/{self.name}"

    @property
    def plugin_file(self) -> Path:
        return self.game.plugins_directory / self.plugin_file_name

    def get_latest_cached_version(self, cache_directory: Path) -> Version | None:
        latest_cached = None
        for entry in cache_directory.glob(f"{self.game_id}-{self.source_name}-{self.name}-*.zip"):
            if not entry.is_file():
                continue
            match = ARCHIVE_FILENAME_PATTERN.match(entry.name)
            if match is None:
                continue
            version = Version.from_tag(match.group("version"))
            if latest_cached is None or version > latest_cached:
                latest_cached = version
        return latest_cached

    def is_cached(self, cache_directory: Path) -> bool:
        return self.get_latest_cached_version(cache_directory) is not None

    def is_installed(self) -> bool:
        return self.installation is not None

    def state(self, cache_directory: Path) -> ModState:
        if self.is_cached(cache_directory):
            if self.is_installed():
                return ModState.INSTALLED
            return ModState.CACHED
        return ModState.NONE


from blasmodcli.model.authorship import Authorship
from blasmodcli.model.dependency import Dependency
from blasmodcli.model.game import Game
from blasmodcli.model.mod_installation import ModInstallation
from blasmodcli.model.mod_source import ModSource
