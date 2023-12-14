import json

class FncsBridgeResponse:
    def __init__(self):
        self.timestamp = 0
        self.command = ""
        self.response = ""
        self.output = {}

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_command(self):
        return self.command

    def set_command(self, command):
        self.command = command

    def get_response(self):
        return self.response

    def set_response(self, response):
        self.response = response

    def get_output(self):
        return self.output

    def set_output(self, output):
        self.output = output

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if "command" not in obj:
            raise ValueError("Expected attribute 'command' not found")
        response = FncsBridgeResponse()
        response.__dict__.update(obj)
        return response
