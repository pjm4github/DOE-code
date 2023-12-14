import json
from typing import Dict, Any


class RequestAppStart:
    serial_version_UID = 1

    def __init__(self, app_id: str=None, runtime_options: Dict[str, Any]=None, simulation_id: str=None):
        self.app_id = app_id
        self.runtime_options = runtime_options
        self.simulation_id = simulation_id

    def get_app_id(self):
        return self.app_id
    
    def set_app_id(self, app_id):
        self.app_id = app_id
        
    def get_runtime_options(self):
        return self.runtime_options
    
    def set_runtime_options(self, runtime_options):
        self.runtime_options = runtime_options
    
    def get_simulation_id(self):
        return self.simulation_id
    
    def set_simulation_id(self, simulation_id):
        self.simulation_id = simulation_id
        
    def __str__(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def parse(json_string):
        obj = RequestAppStart(**json.loads(json_string))
        if obj.app_id is None:
            raise ValueError("Expected attribute id not found")
        return obj
