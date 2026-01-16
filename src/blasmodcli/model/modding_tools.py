from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model import Base


class ModdingTools(Base):
    __tablename__ = "modding_tools"

    game_id: Mapped[str] = mapped_column(ForeignKey("game.id"), primary_key=True)
    game: Mapped['Game'] = relationship("Game", back_populates="modding_tools")

    mod_loader: Mapped[str]
    format: Mapped[str]
    url: Mapped[str]
    author: Mapped[str]


from blasmodcli.model.game import Game
