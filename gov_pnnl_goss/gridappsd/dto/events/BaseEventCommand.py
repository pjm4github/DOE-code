# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

class BaseEventCommand:
    serial_version_UID = -1685736716041726260

    def __init__(self):
        self.command = None
        self.simulation_id = None

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['command'] is None:
            raise RuntimeError("Expected attribute object not found")
        return obj
