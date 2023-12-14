
from gov_pnnl_goss.core.Error import Error
from gov_pnnl_goss.core.Response import Response


class ResponseError(Response, Error):
    serial_version_UID = -6531221350777233341

    def __init__(self, message=None):
        super().__init__()
        self.message = message

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
