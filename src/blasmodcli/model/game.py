from pathlib import Path
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base
from blasmodcli.model.path import PathType
from blasmodcli.utils import Directories


class Game(Base):
    __tablename__ = "game"

    name: Mapped[str] = mapped_column(primary_key=True)
    mod_loader: Mapped[str]
    modding_tools_url: Mapped[str]
    linux_native: Mapped[bool]
    saves_directory: Mapped[Path] = mapped_column(PathType)

    sources: Mapped[List['ModSource']] = relationship("ModSource", back_populates="game")

    @property
    def directory(self) -> Path:
        return Directories.get_steam_game_directory(self.name)

    @property
    def modding_directory(self) -> Path:
        return self.directory / "Modding"

    @property
    def plugins_directory(self) -> Path:
        return self.modding_directory / "plugins"


from blasmodcli.model.mod_source import ModSource
