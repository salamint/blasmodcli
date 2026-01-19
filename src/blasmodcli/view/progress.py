from blasmodcli.model import Version
from blasmodcli.utils import Color


class Progress:

    def __init__(self):
        self.__status = None

    def status(self, status: str, color: 'Color'):
        if self.__status is not None:
            return
        print(f" {Color.fmt(status, color)}", flush=True)
        self.__status = status

    def boolean(self, boolean: bool):
        if boolean:
            self.success()
        else:
            self.failure()

    def failure(self):
        self.status("FAILURE", Color.RED)

    def success(self):
        self.status("SUCCESS", Color.GREEN)

    def version(self, version: 'Version'):
        self.status(str(version), Color.YELLOW)

    def has_succeeded(self) -> bool:
        return self.__status is not None and self.__status
