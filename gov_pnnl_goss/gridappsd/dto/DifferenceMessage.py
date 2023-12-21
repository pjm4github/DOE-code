import json

class difference_message:
    def __init__(self):
        self.timestamp = 0
        self.difference_mrid = ""
        self.forward_differences = []
        self.reverse_differences = []

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_json_element(self):
        return json.loads(self.to_"")

    @staticmethod
    def parse(jsonString):
        obj = json.loads(jsonString)
        if obj["difference_mrid"] is None:
            raise RuntimeError("Expected attribute difference_mrid not found")
        return obj
