

from gov_pnnl_goss.core.Request import Request


class UploadRequest(Request):
    def __init__(self, data, data_type):
        super().__init__()
        self.data = data
        self.data_type = data_type

    def get_id(self):
        return self.id

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_data_type(self):
        return self.data_type

    def set_data_type(self, data_type):
        self.data_type = data_type
