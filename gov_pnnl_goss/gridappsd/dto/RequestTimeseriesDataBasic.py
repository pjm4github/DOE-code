
import json
import traceback
from json import JSONDecodeError
from typing import Dict

from gov_pnnl_goss.gridappsd.dto.RequestTimeseriesData import RequestTimeseriesData


class RequestTimeseriesDataBasic(RequestTimeseriesData):

    def __init__(self):
        super().__init__()
        self.query_filter: Dict[str, object] = {}

    def get_query_filter(self):
        return self.query_filter

    def set_query_filter(self, query_filter):
        self.query_filter = query_filter

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        try:
            obj = json.loads(json_string)
        except JSONDecodeError as e:
            raise ValueError("Request time series data request could not be parsed: " + e)
        # if(obj!=null && obj.queryMeasurement.equals("simulation"))
        # 	if(obj.queryFilter==null || !obj.queryFilter.containsKey("simulation_id"))
        # 		throw new JsonSyntaxException("Expected filter simulation_id not found.");
        return obj
