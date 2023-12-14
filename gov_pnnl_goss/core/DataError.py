
from gov_pnnl_goss.core.Error import Error
import json

class DataError(Error):

    def __init__(self, message: str = None):
        super().__init__()
        self._message = message

    def get_message(self):
        return self._message

    def set_message(self, message):
        self._message = message

    def __str__(self):
        return json.dumps(self.__dict__)
