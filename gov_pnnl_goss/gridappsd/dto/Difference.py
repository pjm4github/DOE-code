import json

class difference:
    def __init__(self):
        self.object = ''
        self.attribute = ''
        self.value = ''
        
    def __str__(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['object'] is None:
            raise RuntimeError("Expected attribute object not found")
        return obj
