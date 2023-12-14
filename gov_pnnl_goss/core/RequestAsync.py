
from gov_pnnl_goss.core.Request import Request


class RequestAsync(Request):
    
    serial_version_UID = -7613047700580927505

    def __init__(self):
        super().__init__()
        self._frequency = 0
    
    def get_frequency(self):
        return self._frequency
    
    def set_frequency(self, frequency):
        self._frequency = frequency
