import json

class PowergridModelDataPutRequest:
    
    class Request_type:
        PUT_MODEL = "PUT_MODEL"
    
    class Result_format:
        JSON = "JSON"
        XML = "XML"
        
    def __init__(self):
        self.request_type = None
        self.model_id = None
        self.input_format = None
        self.model_content = None
        
    def get_model_id(self):
        return self.model_id
    
    def set_model_id(self, model_id):
        self.model_id = model_id
        
    def get_request_type(self):
        return self.request_type
    
    def set_request_type(self, request_type):
        self.request_type = request_type
    
    def get_input_format(self):
        return self.input_format
    
    def set_input_format(self, input_format):
        self.input_format = input_format
    
    def get_model_content(self):
        return self.model_content
    
    def set_model_content(self, model_content):
        self.model_content = model_content
    
    def __str__(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def parse(json_string):
        obj = PowergridModelDataPutRequest()
        parsed_data = json.loads(json_string)
        
        obj.request_type = parsed_data.get('request_type', None)
        obj.model_id = parsed_data.get('model_id', None)
        obj.input_format = parsed_data.get('input_format', None)
        obj.model_content = parsed_data.get('model_content', None)
        
        if obj.request_type is None:
            raise ValueError("Expected attribute requestType not found: " + json_string)
            
        return obj
