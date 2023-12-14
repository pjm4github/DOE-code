import json
import os
from typing import List, Dict

class ServiceInfo:
    class ServiceType:
        PYTHON = "PYTHON"
        JAVA = "JAVA"
        WEB = "WEB"
        EXE = "EXE"

    class ServiceCategory:
        SIMULATOR = "SIMULATOR"
        COSIMULATOR = "COSIMULATOR"
        SERVICE = "SERVICE"

    def __init__(self):
        self.id = ""
        self.description = ""
        self.creator = ""
        self.input_topics = []
        self.output_topics = []
        self.static_args = []
        self.execution_path = ""
        self.user_input = {}  # Dictionary with string keys and UserOptions values
        self.type = ""
        self.launch_on_startup = False
        self.service_dependencies = []
        self.multiple_instances = False
        self.environment_variables = []  # List of EnvironmentVariable objects
        self.category = ServiceInfo.ServiceCategory.SERVICE

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_creator(self):
        return self.creator

    def set_creator(self, creator):
        self.creator = creator

    def get_input_topics(self):
        return self.input_topics

    def set_input_topics(self, input_topics):
        self.input_topics = input_topics

    def get_output_topics(self):
        return self.output_topics

    def set_output_topics(self, output_topics):
        self.output_topics = output_topics

    def get_static_args(self):
        return self.static_args

    def set_static_args(self, static_args):
        self.static_args = static_args

    def get_execution_path(self):
        return self.execution_path

    def set_execution_path(self, execution_path):
        self.execution_path = execution_path

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def is_launch_on_startup(self):
        return self.launch_on_startup

    def set_launch_on_startup(self, launch_on_startup):
        self.launch_on_startup = launch_on_startup

    def get_service_dependencies(self):
        return self.service_dependencies

    def set_service_dependencies(self, service_dependencies):
        self.service_dependencies = service_dependencies

    def is_multiple_instances(self):
        return self.multiple_instances

    def set_multiple_instances(self, multiple_instances):
        self.multiple_instances = multiple_instances

    def get_environment_variables(self):
        return self.environment_variables

    def set_environment_variables(self, environment_variables):
        self.environment_variables = environment_variables

    def get_category(self):
        return self.category

    def set_category(self, category):
        self.category = category

    def __str__(self):
        #return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if "voltage_id" not in obj:
            raise ValueError("Expected attribute 'voltage_id' not found")
        service_info = ServiceInfo()
        service_info.__dict__.update(obj)
        return service_info

if __name__ == "__main__":
    # Example usage: parse a JSON file and print the parsed object
    file_path = "../services/ochre.config"
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            json_data = file.read()
            service_info = ServiceInfo.parse(json_data)
            print(service_info.to_json())
    else:
        print(f"File not found: {file_path}")
