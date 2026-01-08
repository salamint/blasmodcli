from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base


class Authorship(Base):
    __tablename__ = "authorship"

    mod_id: Mapped[int] = mapped_column(ForeignKey("mod.id"), primary_key=True)
    mod: Mapped['Mod'] = relationship("Mod", back_populates="authors")

    name: Mapped[str] = mapped_column(primary_key=True)


from blasmodcli.model.mod import Mod
