import json

class RemoteApplicationExecArgs:
    def __init__(self):
        self.command = None

    def get_command(self):
        return self.command

    def set_command(self, command):
        self.command = command

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['command'] is None:
            raise ValueError("Expected attribute 'command' not found")
        return obj
