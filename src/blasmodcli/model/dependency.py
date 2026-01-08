from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from blasmodcli.model.base import Base


class Dependency(Base):
    __tablename__ = "dependency"

    mod_id: Mapped[int] = mapped_column(ForeignKey("mod.id"), primary_key=True)
    mod: Mapped['Mod'] = relationship("Mod", back_populates="dependencies", foreign_keys=[mod_id])

    dependency_id: Mapped[int] = mapped_column(ForeignKey("mod.id"), primary_key=True)
    dependency: Mapped['Mod'] = relationship("Mod", back_populates="required_by", foreign_keys=[dependency_id])

    minimum_version_id: Mapped[int | None] = mapped_column(ForeignKey("version.id"), default=None)
    minimum_version: Mapped['Version'] = relationship("Version", foreign_keys=[minimum_version_id])

    maximum_version_id: Mapped[int | None] = mapped_column(ForeignKey("version.id"), default=None)
    maximum_version: Mapped['Version'] = relationship("Version", foreign_keys=[maximum_version_id])


from blasmodcli.model.mod import Mod
from blasmodcli.model.version import Version
