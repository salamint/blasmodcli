from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from blasmodcli.model.base import Base
from blasmodcli.model.version import Version, VersionType


class Dependency(Base):
    __tablename__ = "dependency"

    mod_id: Mapped[int] = mapped_column(ForeignKey("mod.id"), primary_key=True)
    mod: Mapped['Mod'] = relationship("Mod", back_populates="dependencies", foreign_keys=[mod_id])

    dependency_id: Mapped[int] = mapped_column(ForeignKey("mod.id"), primary_key=True)
    dependency: Mapped['Mod'] = relationship("Mod", back_populates="required_by", foreign_keys=[dependency_id])

    minimum_version: Mapped[Optional['Version']] = mapped_column(VersionType, default=None)
    maximum_version: Mapped[Optional['Version']] = mapped_column(VersionType, default=None)


from blasmodcli.model.mod import Mod
