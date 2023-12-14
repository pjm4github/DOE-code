# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

from enum import Enum


class RequestType(Enum):
    new_events = 1
    update_events = 2
    query_events = 3


class RequestTestUpdate:
    
    serial_version_UID = 1

    def __init__(self):
        self.command = None
        self.events = []

    def get_command(self):
        return self.command

    def set_command(self, command):
        self.command = command

    def get_events(self):
        return self.events

    def set_events(self, events):
        self.events = events

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        return json.loads(json_string, cls=RequestTestUpdate)
