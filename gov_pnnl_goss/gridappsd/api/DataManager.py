from abc import ABC, abstractmethod
from typing import List, Type, TypeVar

from serializable import Serializable

from gov_pnnl_goss.gridappsd.api.DataManagerHandler import DataManagerHandler
from gov_pnnl_goss.gridappsd.api.GridAppsDataHandler import GridAppsDataHandler
from gov_pnnl_goss.gridappsd.data.conversion import DataFormatConverter
from gov_pnnl_goss.core import Response

T = TypeVar('T')

class DataManager(ABC):
    @abstractmethod
    def get_handlers(self, request_class: Type[T]) -> List[GridAppsDataHandler]:
        pass

    @abstractmethod
    def get_handler(self, request_class: Type[T], handler_class: Type[GridAppsDataHandler]) -> GridAppsDataHandler:
        pass

    @abstractmethod
    def get_all_handlers(self) -> List[GridAppsDataHandler]:
        pass

    @abstractmethod
    def register_handler(self, handler: GridAppsDataHandler, request_class: Type[T]) -> None:
        pass

    @abstractmethod
    def register_data_manager_handler(self, handler: DataManagerHandler, name: str) -> None:
        pass

    @abstractmethod
    def process_data_request(self, request: Serializable, type: str, simulation_id: str,
                             temp_data_path: str, username: str) -> Response:
        pass

    @abstractmethod
    def register_converter(self, input_format: str, output_format: str, converter: DataFormatConverter) -> None:
        pass

    @abstractmethod
    def get_converter(self, input_format: str, output_format: str) -> DataFormatConverter:
        pass
