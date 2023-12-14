
from typing import TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')

class DatabaseResult(ABC):
    @abstractmethod
    def populate_from_result(self, result) -> None:
        pass
