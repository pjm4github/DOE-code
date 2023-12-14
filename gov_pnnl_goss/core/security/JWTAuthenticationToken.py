
import json


class JwtAuthenticationToken:
    serial_version_UID = -6203085918969990507

    def __init__(self):
        self._sub = None
        self._nbf = 0
        self._iss = None
        self._exp = 0
        self._iat = 0
        self._jti = None
        self._roles = []

    def get_sub(self):
        return self._sub

    def set_sub(self, sub):
        self._sub = sub

    def get_nbf(self):
        return self._nbf

    def set_nbf(self, nbf):
        self._nbf = nbf

    def get_iss(self):
        return self._iss

    def set_iss(self, iss):
        self._iss = iss

    def get_exp(self):
        return self._exp

    def set_exp(self, exp):
        self._exp = exp

    def get_iat(self):
        return self._iat

    def set_iat(self, iat):
        self._iat = iat

    def get_jti(self):
        return self._jti

    def set_jti(self, jti):
        self._jti = jti

    def get_roles(self):
        return self._roles

    def set_roles(self, roles):
        self._roles = roles

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj._sub is None:
            raise ValueError("Expected attribute sub not found")
        return obj
