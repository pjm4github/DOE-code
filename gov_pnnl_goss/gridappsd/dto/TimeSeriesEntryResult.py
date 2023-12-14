# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

class TimeSeriesEntryResult:
    def __init__(self):
        self.data = None

    def get_data(self):
        if self.data is None:
            self.data = []
        return self.data

    def set_data(self, data):
        self.data = data

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        data = json.loads(json_string)
        obj = TimeSeriesEntryResult()
        obj.set_data(data)
        if obj.data is None:
            raise ValueError("Expected attribute measurements not found")
        return obj
