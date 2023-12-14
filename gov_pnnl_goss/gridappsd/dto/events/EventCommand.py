# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

from gov_pnnl_goss.gridappsd.dto.events.BaseEventCommand import BaseEventCommand


class EventCommand(BaseEventCommand):

    serial_version_UID = -1611073142106355216

    def __init__(self, command, simulation_id, message):
        super().__init__()
        self.command = command
        self.simulation_id = simulation_id
        self.message = message

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_json_element(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj.get('message') is None:
            raise RuntimeError("Expected attribute 'message' not found")
        return obj
