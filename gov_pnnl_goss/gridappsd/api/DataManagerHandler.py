from abc import ABC, abstractmethod
from typing import Any


class DataManagerHandler(ABC):
    @abstractmethod
    def handle(self, request_content: Any, process_id: str, username: str) -> Any:
        pass
