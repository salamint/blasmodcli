from blasmodcli.utils import Color
from blasmodcli.view.message import Message


def confirmation(message: str, default: bool = True):
    Message.print(Color.YELLOW, message, nl=False)
    if default:
        string = "Y/n"
    else:
        string = "y/N"
    response = input(f" [{string}] ").lower()

    if response == "":
        return default
    return response == "y" or response == "yes"
