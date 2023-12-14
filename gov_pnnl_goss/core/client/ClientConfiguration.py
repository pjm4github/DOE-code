
import logging
from collections import defaultdict

from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class ClientConfiguration:
    
    def __init__(self):
        self.logger = LogManager(ClientConfiguration.__name__)
        self.config = defaultdict()
        
    def set(self, key, value):
        self.config[key] = value
        return self
    
    def get(self, key):
        return self.config.get(key)
    
    def get_as_string(self, key):
        return str(self.get(key))
