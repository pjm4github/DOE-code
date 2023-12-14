# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

class UserToken:
    serial_version_UID = -6949464126224009033

    def __init__(self):
        self.sub = ""
        self.nbf = 0
        self.roles = []
        self.iss = ""
        self.exp = 0
        self.iat = 0
        self.jti = ""

    def get_sub(self):
        return self.sub

    def set_sub(self, sub):
        self.sub = sub

    def get_nbf(self):
        return self.nbf

    def set_nbf(self, nbf):
        self.nbf = nbf

    def get_roles(self):
        return self.roles

    def set_roles(self, roles):
        self.roles = roles

    def get_iss(self):
        return self.iss

    def set_iss(self, iss):
        self.iss = iss

    def get_exp(self):
        return self.exp

    def set_exp(self, exp):
        self.exp = exp

    def get_iat(self):
        return self.iat

    def set_iat(self, iat):
        self.iat = iat

    def get_jti(self):
        return self.jti

    def set_jti(self, jti):
        self.jti = jti

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['sub'] is None:
            raise ValueError("Expected attribute sub not found")
        user_token = UserToken()
        user_token.__dict__ = obj
        return user_token

