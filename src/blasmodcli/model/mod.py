from datetime import date
from typing import List, Self

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from blasmodcli.model.authorship import Authorship
from blasmodcli.model.base import Base
from blasmodcli.model.dependency import Dependency
from blasmodcli.model.game import Game
from blasmodcli.model.mod_source import ModSource
from blasmodcli.model.version import Version


class Mod(Base):
    __tablename__ = "mod"
    __table_args__ = (
        UniqueConstraint("source", "repository", name="unique_repository_per_source"),
        UniqueConstraint("source", "plugin_file", name="unique_plugin_file_per_source"),
    )

    game_name: Mapped[str] = mapped_column(ForeignKey("Game.name"), primary_key=True)
    game: Mapped['Game'] = relationship("Game")

    source_name: Mapped[str] = mapped_column(ForeignKey("ModSource.name"), primary_key=True)
    source: Mapped['ModSource'] = relationship("ModSource", back_populates="mods")

    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]
    release_date: Mapped[date]
    repository: Mapped[str]

    version_id: Mapped[int] = mapped_column(ForeignKey(Version.id))
    version: Mapped[Version] = relationship(Version)

    plugin_file_name: Mapped[str]

    dependencies: Mapped[List[Self]] = relationship(Dependency, back_populates="mod_name")
    required_by: Mapped[List[Self]] = relationship(Dependency, back_populates="dependency_name")

    authors: Mapped[List['Authorship']] = relationship("Authorship", back_populates="mod")
