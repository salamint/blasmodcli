from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base
from blasmodcli.model.game import Game
from blasmodcli.model.mod import Mod
from blasmodcli.model.mod_source import ModSource


class Authorship(Base):
    __tablename__ = "authorship"

    game_name: Mapped[str] = mapped_column(ForeignKey("Game.name"), primary_key=True)
    game: Mapped['Game'] = relationship("Game")

    source_name: Mapped[str] = mapped_column(ForeignKey("ModSource.name"), primary_key=True)
    source: Mapped['ModSource'] = relationship("ModSource")

    mod_name: Mapped[str] = mapped_column(ForeignKey("Mod.name"), primary_key=True)
    mod: Mapped['Mod'] = relationship("Mod", back_populates="authors")

    name: Mapped[str] = mapped_column(primary_key=True)
