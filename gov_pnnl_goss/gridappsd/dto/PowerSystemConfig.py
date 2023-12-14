import json

class PowerSystemConfig:
    # TODO change to be a dto rather than full implementation of getters and setters.
    def __init__(self, geographical_region_name="", sub_geographical_region_name="", line_name=""):
        self.geographical_region_name = geographical_region_name
        self.sub_geographical_region_name = sub_geographical_region_name
        self.line_name = line_name
    
    @property
    def geographical_region_name(self):
        return self._geographical_region_name
    
    @geographical_region_name.setter
    def geographical_region_name(self, value):
        self._geographical_region_name = value
    
    @property
    def sub_geographical_region_name(self):
        return self._sub_geographical_region_name
    
    @sub_geographical_region_name.setter
    def sub_geographical_region_name(self, value):
        self._sub_geographical_region_name = value
    
    @property
    def line_name(self):
        return self._line_name
    
    @line_name.setter
    def line_name(self, value):
        self._line_name = value
    
    def __str__(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def parse(json_string):
        data = json.loads(json_string)
        if data['line_name'] is None:
            raise ValueError("Expected attribute line_name not found")
        return PowerSystemConfig(data['GeographicalRegion_name'], data['SubGeographicalRegion_name'], data['Line_name'])
