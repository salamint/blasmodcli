from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from blasmodcli.model.base import Base
from blasmodcli.model.mod import Mod
from blasmodcli.model.version import Version


class Dependency(Base):
    __tablename__ = "dependency"

    mod_name: Mapped[str] = mapped_column(ForeignKey(Mod.name), primary_key=True)
    mod: Mapped[Mod] = relationship(Mod, back_populates="dependencies")

    dependency_name: Mapped[str] = mapped_column(ForeignKey(Mod.name), primary_key=True)
    dependency: Mapped[Mod] = relationship(Mod, back_populates="required_by")

    minimum_version_id: Mapped[int | None] = mapped_column(ForeignKey(Version.id), default=None)
    minimum_version: Mapped[Version] = relationship(Version)
    maximum_version_id: Mapped[int | None] = mapped_column(ForeignKey(Version.id), default=None)
    maximum_version: Mapped[Version] = relationship(Version)
