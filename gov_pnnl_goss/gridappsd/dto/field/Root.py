# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

from gov_pnnl_goss.gridappsd.dto.field.Feeder import Feeder


class Root:
    serial_version_UID = 1

    def __init__(self):
        self.feeders = Feeder()

    def __str__(self):
        return json.dumps(self.__dict__)

