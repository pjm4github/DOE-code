import json
import os
from typing import List, Dict

class RequestSimulation:
    class SimulationRequestType:
        NEW = "NEW"
        PAUSE = "PAUSE"
        RESUME = "RESUME"
        STOP = "STOP"

    class PowerSystemConfig:
        def __init__(self):
            pass  # Define the fields of PowerSystemConfig here

    class SimulationConfig:
        def __init__(self):
            pass  # Define the fields of SimulationConfig here

    class ApplicationConfig:
        def __init__(self):
            pass  # Define the fields of ApplicationConfig here

    class TestConfig:
        def __init__(self):
            pass  # Define the fields of TestConfig here

    def __init__(self):
        self.power_system_config = None  # Initialize as a PowerSystemConfig object
        self.simulation_config = None  # Initialize as a SimulationConfig object
        self.application_config = None  # Initialize as an ApplicationConfig object or None
        self.service_configs = []  # List of ServiceConfig objects
        self.test_config = None  # Initialize as a TestConfig object or None
        self.simulation_request_type = RequestSimulation.SimulationRequestType.NEW
        self.simulation_id = ""  # Used for pause/resume/stop requests

    def get_power_system_config(self):
        return self.power_system_config

    def set_power_system_config(self, power_system_config):
        self.power_system_config = power_system_config

    def get_simulation_config(self):
        return self.simulation_config

    def set_simulation_config(self, simulation_config):
        self.simulation_config = simulation_config

    def get_application_config(self):
        if self.application_config is None:
            return RequestSimulation.ApplicationConfig()
        return self.application_config

    def set_application_config(self, application_config):
        self.application_config = application_config

    def get_simulation_request_type(self):
        return self.simulation_request_type

    def set_simulation_request_type(self, simulation_request_type):
        self.simulation_request_type = simulation_request_type

    def get_simulation_id(self):
        return self.simulation_id

    def set_simulation_id(self, simulation_id):
        self.simulation_id = simulation_id

    def get_test_config(self):
        return self.test_config

    def set_test_config(self, test_config):
        self.test_config = test_config

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if "power_system_config" not in obj:
            raise ValueError("Expected attribute 'power_system_config' not found")
        if obj.get("test_config"):
            for event in obj["test_config"]["events"]:
                if "occuredDateTime" not in event or "stopDateTime" not in event:
                    raise RuntimeError("Expected attribute 'occuredDateTime' or 'stopDateTime' not found")
                if event["occuredDateTime"] >= event["stopDateTime"]:
                    raise RuntimeError("occuredDateTime cannot be greater than or equal to stopDateTime for an event")
        request_simulation = RequestSimulation()
        request_simulation.__dict__.update(obj)
        return request_simulation

if __name__ == "__main__":
    # Example usage: parse a JSON file and print the parsed object
    file_path = "../your_file_path_here.json"
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            json_data = file.read()
            request_simulation = RequestSimulation.parse(json_data)
            print(request_simulation.to_json())
    else:
        print(f"File not found: {file_path}")
