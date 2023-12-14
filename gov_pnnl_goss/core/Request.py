
import uuid

from gov_pnnl_goss.core.Response import RESPONSE_FORMAT


class Request:
    serial_version_UID = 7480441703135671635

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.url = None
        self.response_format = RESPONSE_FORMAT.XML

    def get_id(self):
        return self.id
    
    def get_url(self):
        return self.url
    
    def set_url(self, url):
        self.url = url
    
    def get_response_format(self):
        return self.response_format
    
    def set_response_format(self, response_format):
        self.response_format = response_format
