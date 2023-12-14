import json
from typing import List

class SimulationConfig:
    DEFAULT_SIMULATION_BROKER_PORT = 5570
    DEFAULT_SIMULATION_BROKER_LOCATION = "127.0.0.1"

    def __init__(self):
        self.power_flow_solver_method = ""
        self.duration = 86400
        self.simulation_id = ""
        self.simulation_name = ""
        self.simulator = ""
        self.start_time = 0
        self.run_realtime = True
        self.simulation_output = SimulationOutput()
        self.model_creation_config = ModelCreationConfig()
        self.simulation_broker_port = SimulationConfig.DEFAULT_SIMULATION_BROKER_PORT
        self.simulation_broker_location = SimulationConfig.DEFAULT_SIMULATION_BROKER_LOCATION

    def get_power_flow_solver_method(self):
        return self.power_flow_solver_method

    def set_power_flow_solver_method(self, power_flow_solver_method):
        self.power_flow_solver_method = power_flow_solver_method

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration

    def get_simulation_id(self):
        return self.simulation_id

    def set_simulation_id(self, simulation_id):
        self.simulation_id = simulation_id

    def get_simulation_name(self):
        return self.simulation_name

    def set_simulation_name(self, simulation_name):
        self.simulation_name = simulation_name

    def get_simulator(self):
        return self.simulator

    def set_simulator(self, simulator):
        self.simulator = simulator

    def get_start_time(self):
        return self.start_time

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_run_realtime(self):
        return self.run_realtime

    def set_run_realtime(self, run_realtime):
        self.run_realtime = run_realtime

    def get_simulation_output(self):
        return self.simulation_output

    def set_simulation_output(self, simulation_output):
        self.simulation_output = simulation_output

    def get_model_creation_config(self):
        return self.model_creation_config

    def set_model_creation_config(self, model_creation_config):
        self.model_creation_config = model_creation_config

    def get_simulation_broker_port(self):
        return self.simulation_broker_port

    def set_simulation_broker_port(self, simulation_broker_port):
        self.simulation_broker_port = simulation_broker_port

    def get_simulation_broker_location(self):
        return self.simulation_broker_location

    def set_simulation_broker_location(self, simulation_broker_location):
        self.simulation_broker_location = simulation_broker_location

    #def to_json(self):
        # return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if "simulation_name" not in obj:
            raise ValueError("Expected attribute 'simulation_name' not found")
        return SimulationConfig(**obj)

class SimulationOutput:
    def __init__(self):
        pass  # Define the fields of SimulationOutput here

class ModelCreationConfig:
    def __init__(self):
        pass  # Define the fields of ModelCreationConfig here
