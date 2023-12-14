import json

class AppInstance:
    def __init__(self, instance_id, app_info, runtime_options, request_id, simulation_id, process):
        self.instance_id = instance_id
        self.app_info = app_info
        self.runtime_options = runtime_options
        self.request_id = request_id
        self.simulation_id = simulation_id
        self.process = process

    def get_instance_id(self):
        return self.instance_id

    def set_instance_id(self, instance_id):
        self.instance_id = instance_id

    def get_app_info(self):
        return self.app_info

    def set_app_info(self, app_info):
        self.app_info = app_info

    def get_runtime_options(self):
        return self.runtime_options

    def set_runtime_options(self, runtime_options):
        self.runtime_options = runtime_options

    def get_request_id(self):
        return self.request_id

    def set_request_id(self, request_id):
        self.request_id = request_id

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
