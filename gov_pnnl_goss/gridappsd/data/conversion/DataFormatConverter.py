
from abc import ABC, abstractmethod
from gov_pnnl_goss.gridappsd.dto import RequestTimeseriesData
from typing import IO

class DataFormatConverter(ABC):
    @abstractmethod
    def convert(self, input_content: str, output_content: IO[str], request: RequestTimeseriesData) -> None:
        pass

    @abstractmethod
    def convert_stream(self, input_content: IO[str], output_content: IO[str], request: RequestTimeseriesData) -> None:
        pass
