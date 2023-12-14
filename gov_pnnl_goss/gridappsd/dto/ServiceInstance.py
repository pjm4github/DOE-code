# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

class ServiceInstance:
    def __init__(self, instance_id, service_info, runtime_options, simulation_id, process):
        self.instance_id = instance_id
        self.service_info = service_info
        self.runtime_options = runtime_options
        self.simulation_id = simulation_id
        self.process = process

    def get_instance_id(self):
        return self.instance_id

    def set_instance_id(self, instance_id):
        self.instance_id = instance_id

    def get_service_info(self):
        return self.service_info

    def set_service_info(self, service_info):
        self.service_info = service_info

    def get_runtime_options(self):
        return self.runtime_options

    def set_runtime_options(self, runtime_options):
        self.runtime_options = runtime_options

    def get_simulation_id(self):
        return self.simulation_id

    def set_simulation_id(self, simulation_id):
        self.simulation_id = simulation_id

    def get_process(self):
        return self.process

    def set_process(self, process):
        self.process = process

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['instance_id'] is None:
            raise ValueError("Expected attribute instance_id not found")
        return obj
