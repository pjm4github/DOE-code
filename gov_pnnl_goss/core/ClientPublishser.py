
from abc import ABC, abstractmethod
from typing import Any
from enum import Enum


class ClientPublisher(ABC):

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def send_message(self, message: Any, destination: Any, reply_destination: Any, response_format: Enum) -> None:
        pass

    @abstractmethod
    def publish(self, destination: Any, data: Any) -> None:
        pass

    @abstractmethod
    def publish_blob_message(self, destination: Any, file: Any) -> None:
        pass
