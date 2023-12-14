# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

class RoleRequest:
    serial_version_UID = -3277794121736133832

    def __init__(self):
        self.user = None
        
    def get_user(self):
        return self.user
    
    def set_user(self, user):
        self.user = user
        
    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__)
        
    @staticmethod
    def parse(json_string):
        return json.loads(json_string, object_hook=lambda d: RoleRequest(**d))
