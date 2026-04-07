from blasmodcli.model import Version
from blasmodcli.utils import Color


class Progress:

    def __init__(self):
        self.__status = None

    def status(self, status: str, color: 'Color'):
        if self.__status is not None:
            return
        print(f" {color.fmt(status)}", flush=True)
        self.__status = status

    def boolean(self, boolean: bool):
        if boolean:
            self.success()
        else:
            self.failure()

    def failure(self, message: str | None = None):
        self.status("FAILURE" if message is None else message, Color.RED)

    def success(self, message: str | None = None):
        self.status("SUCCESS" if message is None else message, Color.GREEN)

    def version(self, version: 'Version'):
        self.status(str(version), Color.YELLOW)

    def has_succeeded(self) -> bool:
        return self.__status is not None and self.__status
