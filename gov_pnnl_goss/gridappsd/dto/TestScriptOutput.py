# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json
from json import Gson, JSONDecodeError


class TestScriptOutput:

    def __init__(self):
        self.output_objects = []

    def get_output_objects(self):
        if self.output_objects is None:
            self.output_objects = []
        return self.output_objects

    def set_output_objects(self, output_objects):
        self.output_objects = output_objects

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        try:
            obj = json.loads(json_string)
        except JSONDecodeError as e:
            raise ValueError("Json_string could not be parsed: " + e)
        if obj.output_objects is None:
            raise RuntimeError("Expected attribute output_objects not found")
        return obj
