from dataclasses import dataclass

from blasmodcli.utils import Color


@dataclass
class TableRow:
    header: str
    value: str
    color: Color | None

    def print(self, row_size: int):
        formatted_header = Color.fmt(self.header, Color.WHITE)
        if len(self.header) < row_size:
            formatted_header += " " * (row_size - len(self.header))
        formatted_value = self.value if self.color is None else Color.fmt(self.value, self.color)
        print(formatted_header, formatted_value)


class Table:

    def __init__(self, title: str, row_size: int = 0):
        self.title = title
        self.row_size = row_size
        self.dynamic = row_size <= 0
        self.rows: list[TableRow] = []

    def add_row(self, header: str, value, color: Color | None = None):
        header_size = len(header)
        if self.dynamic and self.row_size < header_size:
            self.row_size = header_size
        self.rows.append(TableRow(header, value, color))

    def print(self):
        print(self.title)
        print("=" * len(self.title))
        for row in self.rows:
            row.print(self.row_size)
