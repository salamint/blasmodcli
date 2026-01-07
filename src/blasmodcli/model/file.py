from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base


class File(Base):
    __tablename__ = "file"

    directory: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(primary_key=True)

    mod_name: Mapped[str] = mapped_column(ForeignKey("ModInstallation.mod_name"))
    mod: Mapped['ModInstallation'] = relationship("ModInstallation", back_populates="files")


from blasmodcli.model.mod_installation import ModInstallation
