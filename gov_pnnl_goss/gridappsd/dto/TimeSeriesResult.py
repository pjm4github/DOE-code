# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

class TimeSeriesResult:
    
    def __init__(self):
        self.data = []
    
    def get_measurements(self):
        return self.data
    
    def set_measurements(self, data):
        self.data = data
    
    def add_measurement(self, data):
        if self.data is None:
            self.data = []
        self.data.append(data)
    
    def __str__(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def from_json(json_string):
        obj = json.loads(json_string)
        if obj['data'] is None:
            raise ValueError("Expected attribute measurements not found")
        return obj
