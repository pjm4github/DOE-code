
import json

class SimulationOutputObject:
    
    def __init__(self):
        self.name = ""
        self.properties = []
    
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_properties(self):
        return self.properties

    def set_properties(self, properties):
        self.properties = properties

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_string):
        obj = json.loads(json_string)
        if obj.get('name') is None:
            raise ValueError("Expected attribute name not found")
        sim_output = SimulationOutputObject()
        sim_output.__dict__.update(obj)
        return sim_output
