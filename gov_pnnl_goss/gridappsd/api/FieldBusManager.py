from abc import ABC, abstractmethod


class FieldBusManager(ABC):
    @abstractmethod
    def handle_request(self, request_queue: str, request):
        pass

    @property
    @abstractmethod
    def field_model_mrid(self) -> str:
        pass
