
from enum import Enum


class ClientErrorCode(Enum):
    
    NULL_REQUEST_ERROR = 401
    
    def __init__(self, number):
        self.number = number
    
    def get_number(self):
        return self.number
