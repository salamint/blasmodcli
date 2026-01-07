from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base
from blasmodcli.model.file import File
from blasmodcli.model.mod import Mod
from blasmodcli.model.version import Version


class ModInstallation(Base):
    __tablename__ = "mod_installation"

    mod_name: Mapped[str] = mapped_column(ForeignKey(Mod.name), primary_key=True)
    mod: Mapped[Mod] = relationship(Mod)

    version_id: Mapped[int] = mapped_column(ForeignKey(Version.id))
    version: Mapped[Version] = relationship(Version)

    datetime: Mapped[datetime]
    files: Mapped[List[File]] = relationship(File, back_populates="mod")
