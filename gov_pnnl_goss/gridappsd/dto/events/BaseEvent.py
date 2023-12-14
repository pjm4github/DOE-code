# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

class BaseEvent:
    serial_version_UID = 4661909217634755114

    def __init__(self):
        self.fault_mrid = None
        self.status = None
        self.time_initiated = None
        self.time_cleared = None

    def build_sim_fault(self):
        """
        /**
        * Build a fault recoginizable by external elements such as the fncs_goss_bridges.py or simulator
        * @return
        */
        :return:
        """
        pass

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['timeInitiated'] is None:
            raise RuntimeError("Expected attribute simulation_id not found")
        return obj
