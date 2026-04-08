from datetime import datetime
from pathlib import Path


class Installation:

    def __init__(self, file: Path, mod_version: 'ModVersion'):
        self.file = file
        self.mod_version = mod_version
        self.files: list['File'] = []

    @property
    def mod(self) -> 'Mod':
        return self.mod_version.mod

    @property
    def version(self) -> 'Version':
        return self.mod_version.version

    def get_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.file.stat().st_mtime)

    def persist(self):
        with self.file.open("w") as fd:
            for file in self.files:
                fd.write(f"{file.hash} {file.relpath}\n")

    def is_broken(self) -> bool:
        for file in self.files:
            if not file.exists():
                return True
        return False

    def delete(self):
        for file in self.files:
            file.path.unlink(missing_ok=True)
        self.file.unlink()


from blasmodcli.model.file import File
from blasmodcli.model.mod import Mod, ModVersion
from blasmodcli.model.version import Version
