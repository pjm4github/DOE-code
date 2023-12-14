# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

class RoleList:
    
    def __init__(self):
        self.roles = []
    
    def get_roles(self):
        return self.roles
    
    def set_roles(self, roles):
        self.roles = roles
    
    def __str__(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def parse(json_string):
        return json.loads(json_string, object_hook=lambda d: RoleList(**d))
