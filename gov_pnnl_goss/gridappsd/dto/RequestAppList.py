import json

from gov_pnnl_goss.core.client.GossClient import JsonSyntaxException


class RequestAppList:
    def __init__(self, list_running_only: bool=False, app_id: str=None):
        self.list_running_only = list_running_only
        self.app_id = app_id

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        if 'id' not in data:
            raise ValueError("Expected attribute id not found")
        return RequestAppList(data['id'], data.get('list_running_only', False))

    def parse(self, json_string:str):
        obj = json.loads(json_string)
        if not obj.app_id:
            raise JsonSyntaxException("Expected attribute id not found")
        return obj