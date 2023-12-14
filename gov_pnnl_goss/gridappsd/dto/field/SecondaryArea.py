# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json


class SecondaryArea:
    serial_version_UID = 1

    def __init__(self):
        self.distribution_transformer = []
        self.addressable_equipment = []
        self.unaddressable_equipment = []
        self.connectivity_node = []
        self.message_bus_id = ""
        
    def __str__(self):
        return json.dumps(self.__dict__)
