import json


class RequestTimeseriesData:
    def __init__(self):
        self.query_measurement = ""
        self.response_format = "JSON"
        self.query_type = "time-series"
        self.simulation_year = 0
        self.original_format = None

    @property
    def query_measurement(self):
        return self._query_measurement

    @query_measurement.setter
    def query_measurement(self, value):
        self._query_measurement = value

    @property
    def response_format(self):
        return self._response_format

    @response_format.setter
    def response_format(self, value):
        self._response_format = value

    @property
    def query_type(self):
        return self._query_type

    @query_type.setter
    def query_type(self, value):
        self._query_type = value

    @property
    def simulation_year(self):
        return self._simulation_year

    @simulation_year.setter
    def simulation_year(self, value):
        self._simulation_year = value

    @property
    def original_format(self):
        return self._original_format

    @original_format.setter
    def original_format(self, value):
        self._original_format = value

    def __str__(self):
        return json.dumps(self.__dict__)
