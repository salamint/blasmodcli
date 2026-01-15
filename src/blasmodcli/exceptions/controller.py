from blasmodcli.exceptions.base import ApplicationException


class ControllerException(ApplicationException):
    pass


class NothingToDoException(ControllerException):
    pass


class UserCancelException(ControllerException):
    pass
