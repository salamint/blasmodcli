from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base
from blasmodcli.model.version import Version, VersionType


class ModInstallation(Base):
    __tablename__ = "mod_installation"

    mod_id: Mapped[int] = mapped_column(ForeignKey("mod.id"), primary_key=True)
    mod: Mapped['Mod'] = relationship("Mod")

    version: Mapped['Version'] = mapped_column(VersionType)
    datetime: Mapped[datetime]
    files: Mapped[List['File']] = relationship("File", back_populates="mod")


from blasmodcli.model.file import File
from blasmodcli.model.mod import Mod
