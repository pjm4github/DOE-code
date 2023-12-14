
from gov_pnnl_goss.core.Response import Response


class UploadResponse(Response):

    def __init__(self, success):
        super().__init__()
        self.success = success
        self.message = None

    def is_success(self):
        return self.success

    def set_success(self, success):
        self.success = success

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
