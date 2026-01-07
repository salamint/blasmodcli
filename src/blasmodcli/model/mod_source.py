from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base


class ModSource(Base):
    __tablename__ = "mod_source"
    __table_args__ = (
        UniqueConstraint("game_name", "url", name="unique_source_url_per_game"),
    )

    game_name: Mapped[str] = mapped_column(ForeignKey("Game.name"), primary_key=True)
    game: Mapped['Game'] = relationship("Game", back_populates="sources")

    name: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str]
    maintainer: Mapped[str]

    mods: Mapped[List['Mod']] = relationship("Mod", back_populates="source")


from blasmodcli.model.game import Game
from blasmodcli.model.mod import Mod
