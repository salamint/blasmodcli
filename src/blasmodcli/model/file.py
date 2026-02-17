from hashlib import file_digest
from pathlib import Path

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blasmodcli.model.base import Base


CHUNK_SIZE = 4096
FILE_HASH_ALGORITHM = "sha256"


def file_hash(file: Path) -> str:
    with file.open("rb") as fd:
        digest = file_digest(fd, FILE_HASH_ALGORITHM)
    return digest.hexdigest()


class File(Base):
    __tablename__ = "file"

    file: Mapped[str] = mapped_column(primary_key=True)
    hash: Mapped[str]

    mod_id: Mapped[str] = mapped_column(ForeignKey("mod_installation.mod_id"))
    mod_installation: Mapped['ModInstallation'] = relationship("ModInstallation", back_populates="files")

    @property
    def path(self) -> Path:
        return self.mod_installation.mod.game.modding_directory / self.file

    def get_current_hash(self) -> str:
        return file_hash(self.path)

    def exists(self) -> bool:
        return self.path.is_file()

    def has_changed(self) -> bool:
        return self.hash != self.get_current_hash()


from blasmodcli.model.mod_installation import ModInstallation
