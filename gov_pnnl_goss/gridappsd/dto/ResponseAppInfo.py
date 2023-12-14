# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json
from typing import List

from gov_pnnl_goss.gridappsd.dto.AppInfo import AppInfo


class ResponseAppInfo:
    serial_version_UID = 1
    def __init__(self, app_info: List[AppInfo]):
        self.app_info = app_info

    def get_app_info(self):
        return self.app_info

    def set_app_info(self, app_info):
        self.app_info = app_info

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj.get('app_info') is None:
            raise ValueError("Expected attribute app_info not found")
        return ResponseAppInfo(obj['app_info'])
