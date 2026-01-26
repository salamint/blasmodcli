from pathlib import Path

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base


class File(Base):
    __tablename__ = "file"

    directory: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(primary_key=True)

    mod_id: Mapped[str] = mapped_column(ForeignKey("mod_installation.mod_id"))
    mod_installation: Mapped['ModInstallation'] = relationship("ModInstallation", back_populates="files")

    @property
    def path(self) -> Path:
        return self.mod_installation.mod.game.modding_directory / self.directory / self.name


from blasmodcli.model.mod_installation import ModInstallation
