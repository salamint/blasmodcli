

class Argument:

    def __init__(self, *names: str, default, type: type, help: str):
        self.names = names
        self.default = default
        self.type = type
        self.help = help
