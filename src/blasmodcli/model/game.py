from pathlib import Path
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base
from blasmodcli.model.path import PathType
from blasmodcli.utils import Directories


class Game(Base):
    __tablename__ = "game"

    id: Mapped[str] = mapped_column(primary_key=True)

    title: Mapped[str]
    developer: Mapped[str]
    publisher: Mapped[str]
    linux_native: Mapped[bool]
    saves_directory: Mapped[Path] = mapped_column(PathType)

    modding_tools: Mapped['ModdingTools'] = relationship("ModdingTools", back_populates="game", cascade="all, delete-orphan")

    sources: Mapped[List['ModSource']] = relationship("ModSource", back_populates="game")

    @property
    def directory(self) -> Path:
        return Directories.get_steam_game_directory(self.title)

    @property
    def modding_directory(self) -> Path:
        return self.directory / "Modding"

    @property
    def plugins_directory(self) -> Path:
        return self.modding_directory / "plugins"


from blasmodcli.model.mod_source import ModSource
from blasmodcli.model.modding_tools import ModdingTools
