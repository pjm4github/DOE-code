
from typing import Optional

from gov_pnnl_goss.core.client.GossClient import ConnectionCode


# from gov_pnnl_goss.core.Error import
# from goss_core.error_code import ErrorCode
# from goss_core.connection_code import ConnectionCode
# from java.util import HashMap, Map


class ExceptionLookup:
    
    def __init__(self):
        self.lookup_map = None

    def initialize(self):
        if self.lookup_map is not None:
            return
        self.lookup_map = {}
        self.lookup_map[self.get_key(ConnectionCode, ConnectionCode.SESSION_ERROR)] = "Could not create a valid session"

    def start(self):
        self.initialize()

    def stop(self):
        self.lookup_map.clear()
        self.lookup_map = None

    def get_key(self, code_class, code) -> str:
        return code_class.__name__ + "__" + code.name

    def get_text(self, code) -> str:
        key = self.get_key(code.__class__, code)
        return self.lookup_map.get(key) or f"An unknown error code: {code} detected"
