from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from blasmodcli.model.base import Base
from blasmodcli.model.version import Version


class Mod(Base):
    __tablename__ = "mod"

    name: Mapped[str] = mapped_column(primary_key=True)
    author: Mapped[str]
    description: Mapped[str]
    release_date: Mapped[date]
    repository: Mapped[str]

    version_id: Mapped[int] = mapped_column(ForeignKey(Version.id))
    version: Mapped[Version] = relationship(Version)
