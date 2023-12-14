import json

class ApplicationObject:
    
    def __init__(self):
        self.name = ""
        self.config_string = ""

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_config_string(self):
        return self.config_string

    def set_config_string(self, config_string):
        self.config_string = config_string

    def __str__(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj["name"] is None:
            raise ValueError("Expected attribute 'name' not found")
        return obj
