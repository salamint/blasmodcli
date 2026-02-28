from dataclasses import dataclass, field, InitVar
from datetime import date
from enum import IntEnum
from pathlib import Path
from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from blasmodcli.model.base import Base
from blasmodcli.model.version import Version, VersionType


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
    game: Mapped['Game'] = relationship("Game", back_populates="mods")

    source_name: Mapped[str] = mapped_column(ForeignKey("source.name"))
    source: Mapped['Source'] = relationship("Source", back_populates="mods")

    name: Mapped[str]
    display_name: Mapped[str]
    description: Mapped[str]
    is_library: Mapped[bool]
    release_date: Mapped[date]
    repository: Mapped[str]
    latest_version: Mapped['Version'] = mapped_column(VersionType)
    plugin_file_name: Mapped[str]
    artifact_name: Mapped[str]

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

    installation: Mapped[Optional['Installation']] = relationship("ModInstallation", back_populates="mod")

    @property
    def is_installed(self) -> bool:
        return self.installation is not None

    @property
    def full_name(self):
        return f"{self.source.name}/{self.name}"

    @property
    def plugin_file(self) -> Path:
        return self.game.plugins_directory / self.plugin_file_name

    def get_download_url(self, version: Version | None = None) -> str:
        version = version if version is not None else self.latest_version
        return f"{self.repository}/releases/download/{version}/{self.artifact_name}"


@dataclass
class ModVersion:
    mod: Mod
    v: InitVar[Version | None] = None
    version: Version = field(init=False)

    def __post_init__(self, v: Version | None):
        if v is None:
            self.version = self.mod.latest_version
        else:
            self.version = v

    def __getitem__(self, index: int) -> Mod | Version:
        if index == 0:
            return self.mod
        elif index == 1:
            return self.version
        raise IndexError


from blasmodcli.model.authorship import Authorship
from blasmodcli.model.dependency import Dependency
from blasmodcli.model.game import Game
from blasmodcli.model.installation import Installation
from blasmodcli.model.source import Source
