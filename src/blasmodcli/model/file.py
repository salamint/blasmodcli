from hashlib import file_digest
from pathlib import Path


CHUNK_SIZE = 4096
FILE_HASH_ALGORITHM = "sha256"


def file_hash(file: Path) -> str:
    with file.open("rb") as fd:
        digest = file_digest(fd, FILE_HASH_ALGORITHM)
    return digest.hexdigest()


class File:

    def __init__(self, installation: Installation, relpath: str, hash_digest: str | None = None):
        self.installation = installation
        self.relpath = relpath
        self.hash = hash_digest if hash_digest is not None else file_hash(self.path)

    @property
    def path(self) -> Path:
        return self.installation.mod.game.modding_directory / self.relpath

    def get_current_hash(self) -> str:
        return file_hash(self.path)

    def exists(self) -> bool:
        return self.path.is_file()

    def has_changed(self) -> bool:
        return self.hash != self.get_current_hash()

    def update_hash(self):
        self.hash = file_hash(self.path)


from blasmodcli.model.installation import Installation
