from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class IRepository(ABC, Generic[T]):

    @abstractmethod
    def get_all(self) -> list[T]:
        pass
