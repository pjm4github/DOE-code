
import json

class application_config:
    def __init__(self):
        self.applications = []

    def get_applications(self):
        return self.applications

    def set_applications(self, applications):
        self.applications = applications

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj["applications"] is None:
            raise ValueError("Expected attribute applications not found")
        return obj
