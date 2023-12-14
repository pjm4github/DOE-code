
import json


class UserOptions:
    serial_version_UID = 1

    def __init__(self):
        self.name = None
        self.help = None
        self.type = None
        self.help_example = None
        self.default_value = None
        self.min_value = None
        self.max_value = None
    
    def __str__(self):
        return json.dumps(self.__dict__)
