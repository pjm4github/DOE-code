import json

class PowergridModelDataRequest:
    
    class RequestType:
        QUERY = "QUERY"
        QUERY_OBJECT = "QUERY_OBJECT"
        QUERY_OBJECT_TYPES = "QUERY_OBJECT_TYPES"
        QUERY_MODEL = "QUERY_MODEL"
        QUERY_MODEL_NAMES = "QUERY_MODEL_NAMES"
        QUERY_MODEL_INFO = "QUERY_MODEL_INFO"
        QUERY_OBJECT_IDS = "QUERY_OBJECT_IDS"
        QUERY_OBJECT_DICT = "QUERY_OBJECT_DICT"
        QUERY_OBJECT_MEASUREMENTS = "QUERY_OBJECT_MEASUREMENTS"
    
    class ResultFormat:
        JSON = "JSON"
        XML = "XML"
        CSV = "CSV"
    
    def __init__(self):
        self.request_type = ""
        self.model_id = ""
        self.result_format = "JSON"
        self.query_string = ""
        self.object_id = ""
        self.filter = ""
        self.object_type = ""
        
    def get_model_id(self):
        return self.model_id
    
    def set_model_id(self, model_id):
        self.model_id = model_id
        
    def get_result_format(self):
        return self.result_format
    
    def set_result_format(self, result_format):
        self.result_format = result_format
        
    def get_query_string(self):
        return self.query_string
    
    def set_query_string(self, query_string):
        self.query_string = query_string
        
    def get_object_id(self):
        return self.object_id
    
    def set_object_id(self, object_id):
        self.object_id = object_id
        
    def get_filter(self):
        return self.filter
    
    def set_filter(self, filter):
        self.filter = filter
        
    def get_request_type(self):
        return self.request_type
    
    def set_request_type(self, request_type):
        self.request_type = request_type
    
    def get_object_type(self):
        return self.object_type
    
    def set_object_type(self, object_type):
        self.object_type = object_type
        
    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['request_type'] == "":
            raise ValueError("Expected attribute request_type not found: " + json_string)
        return obj
