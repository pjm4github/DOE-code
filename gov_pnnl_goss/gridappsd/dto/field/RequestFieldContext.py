# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json


class RequestFieldContext:
    serial_version_UID = -8105887994597368008

    def __init__(self):
        self.model_id = None
        self.area_id = None

    @staticmethod
    def parse(json_string):
        return json.loads(json_string, object_hook=lambda d: RequestFieldContext(**d))

    def __str__(self):
        return json.dumps(self.__dict__)
