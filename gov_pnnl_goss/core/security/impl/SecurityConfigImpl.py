
import random
import logging
import json
from datetime import datetime, timedelta
import uuid
from json import encoder
import jwt

from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class JWTError(Exception):
    pass


class SecurityConfigImpl:
    def __init__(self):
        self.manager_user = None
        self.manager_password = None
        self.use_token = False
        self.shared_key = self.generate_shared_key()
        self.properties = None
        self.logger = LogManager(SecurityConfigImpl.__name__)
        self.issued_by = "GridOPTICS Software System"

    def get_expiration_date(self):
        return 1000 * 60 * 60 * 24 * 5

    def get_issuer(self):
        return self.issued_by

    def update(self, properties):
        if properties is not None:
            self.properties = properties
            self.manager_user = self.get_property('PROP_SYSTEM_MANAGER', None)
            self.manager_password = self.get_property('PROP_SYSTEM_MANAGER_PASSWORD', None)
            secret = self.get_property('PROP_SYSTEM_TOKEN_SECRET', None)
            if secret and secret.strip():
                self.shared_key = secret.encode()
            use_token_str = self.get_property('PROP_SYSTEM_USE_TOKEN', None)
            if use_token_str and use_token_str.strip():
                try:
                    self.use_token = bool(use_token_str)
                except Exception as e:
                    self.logger.error(f"Could not parse use token parameter as boolean in security config: '{use_token_str}'")
    
    def get_property(self, key, default_value):
        ret_value = default_value
        if key and key.strip() and self.properties.get(key) is not None:
            value = str(self.properties[key])
            if not value.startswith("${"):
                ret_value = value
        return ret_value

    def get_manager_user(self):
        return self.manager_user

    def get_manager_password(self):
        return self.manager_password

    def get_use_token(self):
        return self.use_token

    def generate_shared_key(self):
        shared_key = bytearray(random.getrandbits(8) for _ in range(32))
        return bytes(shared_key)

    def get_shared_key(self):
        if self.shared_key is None:
            self.shared_key = self.generate_shared_key()
        return self.shared_key

    def validate_token(self, token):
        # Implementation for token validation
        pass

    def create_token(self, user_id, roles):
        builder = {
            'iss': self.get_issuer(),
            'sub': str(user_id),
            'iat': datetime.utcnow(),
            'nbf': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=self.get_expiration_date()),
            'jti': str(uuid.uuid4()),
            'roles': list(roles)
        }
        token = jwt.encode(builder, self.get_shared_key(), algorithm='HS256')
        return token

    def parse_token(self, token):
        try:
            decoded = jwt.decode(token, self.get_shared_key(), algorithms=['HS256'])
            json_token = json.dumps(decoded)
            token_obj = json.loads(json_token)
            return token_obj
        except JWTError:
            return None
