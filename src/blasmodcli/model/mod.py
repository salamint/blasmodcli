from datetime import date, datetime
from enum import IntEnum
from typing import List
from requests import get as request

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from blasmodcli.model.base import Base
from blasmodcli.model.version import Version, VersionType

AUTHORS_SEPARATOR = " && "


class DateFormat:
    SIMPLE = "%Y-%m-%d"
    DETAILED = "%A, %e %B %Y"


class ModState(IntEnum):
    NONE = 0
    INSTALLED = 1
    ACTIVATED = 2


class Mod(Base):
    __tablename__ = "mod"
    __table_args__ = (
        UniqueConstraint("source_name", "name", name="unique_name_per_source"),
        UniqueConstraint("source_name", "repository", name="unique_repository_per_source"),
        UniqueConstraint("source_name", "plugin_file_name", name="unique_plugin_file_per_source"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    game_name: Mapped[str] = mapped_column(ForeignKey("game.name"))
    game: Mapped['Game'] = relationship("Game")

    source_name: Mapped[str] = mapped_column(ForeignKey("mod_source.name"))
    source: Mapped['ModSource'] = relationship("ModSource", back_populates="mods")

    name: Mapped[str]
    description: Mapped[str]
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

    @classmethod
    def from_raw_data(cls, source: 'ModSource', data: dict):
        repository = f"https://github.com/{data['GithubAuthor']}/{data['GithubRepo']}"
        response = request(f"{repository}/releases/latest")
        response.raise_for_status()
        version = Version.from_string(response.url.split("/")[-1])

        mod = cls(
            game_name=source.game.name,
            source_name=source.name,
            name=data["Name"],
            description=data["Description"],
            release_date=datetime.strptime(data["InitialReleaseDate"], DateFormat.SIMPLE).date(),
            repository=repository,
            plugin_file_name=data["PluginFile"],
        )

        authors = data["Author"].replace(", ", AUTHORS_SEPARATOR).replace(", && ", AUTHORS_SEPARATOR)
        for author in authors.split(AUTHORS_SEPARATOR):
            mod.authors.append(author.strip())

        for dependency in data.get("Dependencies", []):
            mod.dependencies.append(dependency)
        return mod


from blasmodcli.model.authorship import Authorship
from blasmodcli.model.dependency import Dependency
from blasmodcli.model.game import Game
from blasmodcli.model.mod_source import ModSource
