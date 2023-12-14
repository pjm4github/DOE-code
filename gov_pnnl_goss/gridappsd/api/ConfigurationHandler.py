from abc import ABC, abstractmethod
from typing import Dict, TextIO

class ConfigurationHandler(ABC):

    @abstractmethod
    def generate_config(self, parameters: Dict, out: TextIO, process_id: str, username: str) -> None:
        pass
        raise NotImplementedError("Subclasses must implement generate_config method")
