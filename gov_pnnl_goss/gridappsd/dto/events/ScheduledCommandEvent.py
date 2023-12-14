# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

from gov_pnnl_goss.core.Event import Event
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.TestFaultMessage import DifferenceMessage


class ScheduledCommandEvent(Event):
    
    serial_version_UID = 2435694477772334059

    def __init__(self):
        super().__init__()
        self.message = DifferenceMessage()
    
    def set_message(self, dm):
        self.message = dm
    
    def get_message(self):
        return self.message
    
    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj.occured_date_time == 0 or obj.stop_date_time == 0:
            raise RuntimeError("Expected attribute timeInitiated or timeCleared is not found")
        return obj
