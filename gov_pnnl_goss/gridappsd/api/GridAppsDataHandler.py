from abc import ABC, abstractmethod
from typing import List


class GridAppsDataHandler(ABC):
    @abstractmethod
    def handle(self, request, simulation_id: str, temp_data_path: str, log_manager):
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def supported_request_types(self) -> List[type]:
        pass
