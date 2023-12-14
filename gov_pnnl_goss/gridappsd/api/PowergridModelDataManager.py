from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from gov_pnnl_goss.SpecialClasses import ResultSet


class ResultFormat(Enum):
    JSON = "JSON"
    XML = "XML"
    CSV = "CSV"


class PowergridModelDataManager(ABC):

    @abstractmethod
    def query(self, model_id: str, query: str, result_format: str, process_id: str, username: str) -> str:
        pass

    @abstractmethod
    def query_result_set(self, model_id: str, query: str, process_id: str, username: str) -> ResultSet:
        pass

    @abstractmethod
    def query_object(self, model_id: str, mrid: str, result_format: str, process_id: str, username: str) -> str:
        pass

    @abstractmethod
    def query_object_result_set(self, model_id: str, mrid: str, process_id: str, username: str) -> ResultSet:
        pass

    @abstractmethod
    def query_object_types(self, model_id: str, result_format: str, process_id: str, username: str) -> str:
        pass

    @abstractmethod
    def query_object_type_list(self, model_id: str, process_id: str, username: str) -> List[str]:
        pass

    @abstractmethod
    def query_model(self, model_id: str, object_type: str, filter_str: str, result_format: str, process_id: str, username: str) -> str:
        pass

    @abstractmethod
    def query_model_result_set(self, model_id: str, object_type: str, filter_str: str, process_id: str, username: str) -> ResultSet:
        pass

    @abstractmethod
    def query_model_names(self, result_format: str, process_id: str, username: str) -> str:
        pass

    @abstractmethod
    def query_model_name_list(self, process_id: str, username: str) -> List[str]:
        pass

    @abstractmethod
    def query_model_names_and_ids(self, result_format: str, process_id: str, username: str) -> str:
        pass

    @abstractmethod
    def query_model_names_and_ids_result_set(self, process_id: str, username: str) -> ResultSet:
        pass

    @abstractmethod
    def query_object_ids(self, result_format: str, model_id: str, object_type: str, process_id: str, username: str) -> str:
        pass

    @abstractmethod
    def query_object_ids_list(self, model_id: str, object_type: str, process_id: str, username: str) -> List[str]:
        pass

    @abstractmethod
    def query_object_dict_by_type(self, result_format: str, model_id: str, object_type: str, object_id: str, process_id: str, username: str) -> str:
        pass

    @abstractmethod
    def query_object_dict_by_type_result_set(self, model_id: str, object_type: str, object_id: str, process_id: str, username: str) -> ResultSet:
        pass

    @abstractmethod
    def query_measurement_dict_by_object(self, result_format: str, model_id: str, object_type: str, object_id: str, process_id: str, username: str) -> str:
        pass

    @abstractmethod
    def query_measurement_dict_by_object_result_set(self, model_id: str, object_type: str, object_id: str, process_id: str, username: str) -> ResultSet:
        pass

    @abstractmethod
    def put_model(self, model_id: str, model: str, input_format: str, process_id: str, username: str):
        #  Also will need put_object and delete_object
        #  (will need to support the right security permissions)
        pass
