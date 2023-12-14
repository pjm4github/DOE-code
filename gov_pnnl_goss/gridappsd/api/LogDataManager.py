from abc import ABC, abstractmethod
from typing import Any

from LogManager import LogLevel, ProcessStatus


class LogDataManager(ABC):
    @abstractmethod
    def store(
        self,
        source: str,
        process_id: str,
        timestamp: int,
        log_message: str,
        log_level: LogLevel,
        process_status: ProcessStatus,
        username: str,
        process_type: str,
    ) -> None:
        pass

    @abstractmethod
    def query(
        self,
        source: str,
        process_id: str=None,
        timestamp: int=None,
        log_level: LogLevel=None,
        process_status: ProcessStatus=None,
        username: str=None,
        process_type: str=None,
    ) -> Any:
        pass

    # @abstractmethod
    # def query(self, query_string: str) -> Any:
    #     pass

    @abstractmethod
    def store_expected_results(
        self,
        app_id: str,
        test_id: str,
        process_id_one: str,
        process_id_two: str,
        simulation_time: int,
        simulation_time_two: int,
        mrid: str,
        property_name: str,
        expected: str,
        actual: str,
        difference_direction: str,
        difference_mrid: str,
        match: bool,
    ) -> None:
        pass
