import json


class RequestLogMessage:
    serial_version_UID = 1

    def __init__(self):
        self._username = ""
        self._query = ""

    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    def get_query(self):
        return self._query

    def set_query(self, query):
        self._query = query

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        return obj

    def __str__(self):
        return json.dumps(self.__dict__)
