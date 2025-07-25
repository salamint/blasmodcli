from enum import StrEnum


class Color(StrEnum):
    RESET = "\033[0m"
    BLACK = "\033[1;30m"
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[1;34m"
    MAGENTA = "\033[1;35m"
    CYAN = "\033[1;36m"
    WHITE = "\033[1;37m"

    @staticmethod
    def fmt(obj, color: 'Color') -> str:
        return f"{color}{obj}{Color.RESET}"
