import json

from gov_pnnl_goss.gridappsd.dto.AppInfo import AppInfo


class RequestAppRegister:
    serial_version_UID = 1

    def __init__(self, app_info: AppInfo, app_package: str):
        self.app_info = app_info
        self.app_package = app_package

    def get_app_info(self):
        return self.app_info

    def set_app_info(self, app_info):
        self.app_info = app_info

    def get_app_package(self):
        return self.app_package

    def set_app_package(self, app_package):
        self.app_package = app_package

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['app_info'] == None:
            raise ValueError("Expected attribute app_info not found")
        return obj
