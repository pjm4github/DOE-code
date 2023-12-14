# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

from gov_pnnl_goss.SpecialClasses import Gson
from gov_pnnl_goss.gridappsd.dto.events.BaseEventCommand import BaseEventCommand
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.TestManagerEventsTest import Fault


class FaultCommand(BaseEventCommand):
    
    serial_version_UID = -1611073142106355216

    def __init__(self):
        super().__init__()
        self.message = Fault()
    
    def __str__(self):
        return json.dumps(self.__dict__)
    
    def to_json_element(self):
        gson = Gson()
        return gson.toJsonTree(self)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string, cls=FaultCommand)
        if obj.command is None:
            raise RuntimeError("Expected attribute object not found")
        return obj
