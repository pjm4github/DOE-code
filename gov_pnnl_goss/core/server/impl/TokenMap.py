
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

from gov_pnnl_goss.core.security.impl.SystemRealm import ConcurrentHashMap


class MapItem:
    def __init__(self, ip_address, token, identifier):
        self.last_requested = datetime.now()
        self.token = token
        self.ip_address = ip_address
        self.identifier = identifier

    def update_time(self):
        self.last_requested = datetime.now()


class TokenMap:
    
    def __init__(self):
        self.ONE_MINUTE_IN_MILLIS = 60000
        self.registered_tokens = ConcurrentHashMap()
        self.timeout_minutes = 5

    def register_identifier(self, ip, identifier):
        token = str(uuid.uuid4())
        self._register_identifier(ip, token, identifier)
        return token

    def _register_identifier(self, ip, token, identifier):
        item = MapItem(ip, token, identifier)
        self.registered_tokens[token] = item

    def get_identifier(self, ip, token):
        identifier = None
        if self._is_valid(ip, token):
            identifier = self.registered_tokens[token].identifier
        return identifier

    def _is_valid(self, ip, token):
        valid = False
        if token in self.registered_tokens:
            item = self.registered_tokens[token]
            if item.ip_address == ip and item.token == token:
                before_time = datetime.now() + timedelta(minutes=self.timeout_minutes)
                if item.last_requested < before_time:
                    item.update_time()
                    valid = True
        return valid

