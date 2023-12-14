
import json

class RuleSettings:
    def __init__(self):
        self.name = ""
        self.port = 0
        self.topic = ""
        
    def __str__(self):
        return json.dumps(self.__dict__)
        
    @staticmethod
    def parse(json_string):
        obj = RuleSettings()
        data = json.loads(json_string)
        
        if "name" not in data:
            raise RuntimeError("Expected attribute name not found")
        
        obj.__dict__.update(data)
        return obj
