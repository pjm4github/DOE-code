
from typing import List
import json
from json import JSONDecodeError

from gov_pnnl_goss.gridappsd.dto.RequestTimeseriesData import RequestTimeseriesData


class RequestTimeseriesDataAdvanced(RequestTimeseriesData):
    serial_version_UID = -820277813503252512

    def __init__(self):
        super().__init__()
        self.query_filter = []
        self.select_criteria = []
        self.last = None
        self.first = None

    def get_query_filter(self) -> List[object]:
        return self.query_filter

    def set_query_filter(self, advanced_query_filter: List[object]) -> None:
        self.query_filter = advanced_query_filter

    def get_select_criteria(self) -> List[str]:
        return self.select_criteria

    def set_select_criteria(self, select_criteria: List[str]) -> None:
        self.select_criteria = select_criteria

    def get_last(self) -> int:
        return self.last

    def set_last(self, last: int) -> None:
        self.last = last

    def get_first(self) -> int:
        return self.first

    def set_first(self, first: int) -> None:
        self.first = first

    def __str__(self) -> str:
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string: str) -> 'RequestTimeseriesDataAdvanced':
        import json

        obj = None
        error = ""
        try:
            obj = json.loads(json_string, object_hook=lambda d: Namespace(**d))
        except JSONDecodeError as e:
            error = str(e)
        if not obj:
            raise JSONDecodeError("Request time series data request could not be parsed: " + error, "")
        # if(obj!=null && obj.queryMeasurement.equals("simulation")){
        #   if(obj.queryFilter==null || !obj.queryFilter.containsKey("simulation_id"))
        #      #throw new JsonSyntaxException("Expected filter simulation_id not found.");
        # 	   TODO iterate through and look for key = simulation_id
        return obj
