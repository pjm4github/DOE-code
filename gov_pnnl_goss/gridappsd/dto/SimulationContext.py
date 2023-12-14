import json
from typing import List


class SimulationContext:
    def __init__(self):
        self.simulationId = ""
        self.simulationHost = "127.0.0.1"
        self.simulationPort = 0
        self.simulationDir = ""
        self.startupFile = ""
        self.request = None
        self.simulatorPath = ""
        self.appInstanceIds = []
        self.serviceInstanceIds = []
        self.simulationUser = ""
        self.numFederates = 2

    def get_simulation_id(self):
        return self.simulationId

    def set_simulation_id(self, simulationId):
        self.simulationId = simulationId

    def get_host(self):
        return self.simulationHost

    def set_host(self, host):
        self.simulationHost = host

    def get_port(self):
        return self.simulationPort

    def set_port(self, port):
        self.simulationPort = port

    def get_simulation_dir(self):
        return self.simulationDir

    def set_simulation_dir(self, simulationDir):
        self.simulationDir = simulationDir

    def get_startup_file(self):
        return self.startupFile

    def set_startup_file(self, startupFile):
        self.startupFile = startupFile

    def get_request(self):
        return self.request

    def set_request(self, request):
        self.request = request

    def get_simulator_path(self):
        return self.simulatorPath

    def set_simulator_path(self, simulatorPath):
        self.simulatorPath = simulatorPath

    def get_app_instance_ids(self):
        return self.appInstanceIds

    def set_app_instance_ids(self, appInstanceIds):
        self.appInstanceIds = appInstanceIds

    def get_service_instance_ids(self):
        return self.serviceInstanceIds

    def set_service_instance_ids(self, serviceInstanceIds):
        self.serviceInstanceIds = serviceInstanceIds

    def add_service_instance_ids(self, serviceInstanceId):
        self.serviceInstanceIds.append(serviceInstanceId)

    def get_simulation_user(self):
        return self.simulationUser

    def set_simulation_user(self, simulationUser):
        self.simulationUser = simulationUser

    def get_num_federates(self):
        return self.numFederates

    def set_num_federates(self, numFederates):
        self.numFederates = numFederates

    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        return SimulationContext(**obj)
