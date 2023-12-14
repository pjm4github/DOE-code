
from gov_pnnl_goss.core.Response import Response


class ResponseText(Response):
    serial_version_UID = 3101381364901500884

    def __init__(self, text):
        super().__init__()
        self.text = text

    def get_text(self):
        return self.text
