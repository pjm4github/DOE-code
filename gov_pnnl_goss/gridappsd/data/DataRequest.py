# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
# data_request.py
from gov_pnnl_goss.core.Request import Request


class DataRequest(Request):

    def __init__(self):
        super().__init__()
        self.type = None
        self.request_content = None

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_request_content(self):
        return self.request_content

    def set_request_content(self, request_content):
        self.request_content = request_content
