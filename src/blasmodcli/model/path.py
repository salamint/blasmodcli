from pathlib import Path
from typing import Optional

from sqlalchemy import TypeDecorator, String, Dialect


class PathType(TypeDecorator):

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Optional[Path], dialect: Dialect) -> Optional[str]:
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value: Optional[str], dialect: Dialect) -> Optional[Path]:
        if value is None:
            return None
        return Path(value)
