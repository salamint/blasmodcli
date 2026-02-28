from datetime import datetime
from pathlib import Path

from blasmodcli.model.version import Version


class Installation:

    def __init__(self, file: Path, mod: Mod, version: Version, datetime: datetime):
        self.file = file
        self.mod = mod
        self.version = version
        self.datetime = datetime
        self.files: list['File'] = []

    def persist(self):
        with self.file.open("w") as fd:
            for file in self.files:
                fd.write(f"{file.hash} {file.relpath}\n")

    def is_broken(self) -> bool:
        for file in self.files:
            if not file.exists():
                return True
        return False


from blasmodcli.model.file import File
from blasmodcli.model.mod import Mod
