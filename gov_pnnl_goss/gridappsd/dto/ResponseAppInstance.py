# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json
from typing import List

from gov_pnnl_goss.gridappsd.api.AppManager import AppInstance


class ResponseAppInstance:
    serial_version_UID = 1

    def __init__(self, app_instance: List[AppInstance]):
        self.app_instance = app_instance

    def get_app_info(self):
        return self.app_instance

    def set_app_info(self, app_instance):
        self.app_instance = app_instance

    def __str__(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def parse(jsonString):
        obj = json.loads(jsonString)
        if obj.app_instance is None:
            raise ValueError("Expected attribute app_info not found")
        return obj
