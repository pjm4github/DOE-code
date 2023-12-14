import json

class ConfigurationRequest:
    serial_version_UID = -3277794171736103832
    def __init__(self):
        self.configuration_type = None
        self.parameters = None

    def get_configuration_type(self):
        return self.configuration_type

    def set_configuration_type(self, configuration_type):
        self.configuration_type = configuration_type

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, parameters):
        self.parameters = parameters

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj.configuration_type is None:
            raise ValueError(f'Expected attribute configuration_type not found: {json_string}')
        return obj
