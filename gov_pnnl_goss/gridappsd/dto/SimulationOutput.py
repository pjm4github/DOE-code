
import json
from typing import List


class SimulationOutput:
    serial_version_UID = 1

    def __init__(self):
        self.output_objects = []

    def get_output_objects(self):
        if self.output_objects is None:
            self.output_objects = []
        return self.output_objects

    def set_output_objects(self, output_objects: List):
        self.output_objects = output_objects

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_string):
        obj = SimulationOutput()
        data = json.loads(json_string)
        if 'output_objects' not in data:
            raise ValueError("Expected attribute output_objects not found")
        obj.__dict__.update(data)
        return obj
