from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base


class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    mod_loader: Mapped[str]
    modding_tools_url: Mapped[str]
    linux_native: Mapped[bool]
    saves_directory: Mapped[str]

    sources: Mapped[List['ModSource']] = relationship("ModSource", back_populates="game")


from blasmodcli.model.mod_source import ModSource
